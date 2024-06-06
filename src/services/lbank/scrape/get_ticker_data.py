import asyncio
import itertools
import json
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import httpx
import playwright.async_api
from playwright.async_api import async_playwright
from typing_extensions import List, Optional, Tuple, cast
from websocket import create_connection

from src.services.lbank.types_ import (
    Data,
    GetDataWithBrowserHeadersAndCustomRequestsReturnType,
    GetDataWithBrowserHeadersAndCustomRequestsReturnTypeElement,
    MarketDataApiResponse,
    QryAllApiResponse,
    ScrapeResult,
    WSData,
    WSMarketDataOverView,
    WSScrapingResult,
)
from src.utils.utils import split_list, timeit_context

##
# Browser
##


async def login_sequence(page: playwright.async_api.Page):
    #
    await page.goto("https://www.lbank.com/login")

    username_input_xpath = (
        "/html/body/div[1]/section/main/div[2]/div[1]/form/div[1]/div/input"
    )
    username_input = page.locator(f"xpath=/{username_input_xpath}")
    await username_input.wait_for()
    await username_input.fill(os.getenv("LBANK_USERNAME", ""))

    password_input_xpath = (
        "/html/body/div[1]/section/main/div[2]/div[1]/form/div[2]/div[1]/input"
    )
    password_input = page.locator(f"xpath=/{password_input_xpath}")
    await password_input.wait_for()
    await password_input.fill(os.getenv("LBANK_PASSWORD", ""))

    login_button_xpath = "/html/body/div[1]/section/main/div[2]/div[1]/form/button"
    login_button = page.locator(f"xpath=/{login_button_xpath}")
    await login_button.wait_for()
    await login_button.click()

    # successfull login element check (in prod - might require otp from email)
    test_element_xpath = "/html/body/div[1]/section/header/div/div[3]/div[1]/span/img"
    test_element = page.locator(f"xpath=/{test_element_xpath}")
    try:
        await test_element.wait_for(timeout=5000)  # 20 seconds
    except playwright.async_api.TimeoutError:
        await page.screenshot(path="lbank_login_debug_screenshot.jpg")
        raise


async def get_all_symbols() -> List[str]:
    headers = await get_headers(with_login=False)
    all_symbols = get_all_symbols_headers(headers)
    return all_symbols


def get_all_symbols_headers(headers: dict) -> List[str]:
    response: MarketDataApiResponse = httpx.post(
        "https://lbkperp.lbank.com/cfd/instrment/v1/marketData",
        headers=headers,
        json={"ProductGroup": "SwapU"},
    ).json()
    all_symbols = [symbol_info["instrumentID"] for symbol_info in response["data"]]
    return sorted(all_symbols)


async def scrape_market_data_for_symbol(
    headers: dict, symbol: str, semaphore: asyncio.Semaphore
) -> Optional[Data]:
    async with semaphore:
        try:
            async with httpx.AsyncClient() as client:
                url = "https://lbkperp.lbank.com/cfd/agg/v1/sendQryAll"
                body_params = {
                    "productGroup": "SwapU",
                    "instrumentID": symbol,
                    "asset": "USDT",
                }
                response = await client.post(url, headers=headers, json=body_params)
                response_body: QryAllApiResponse = response.json()
            return response_body["data"]
        except Exception as e:
            print(
                f"Failed to run scrape_market_data_for_symbol; for symbol: {symbol}; Error: {e};"
            )


async def get_headers(with_login=True) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        if with_login:
            await login_sequence(page)

        should_finish_before = datetime.now() + timedelta(seconds=10)  # for timeout
        should_finish = False  # flip when time to finish (timeout)
        result: dict = {}  # request response data will be stored here

        async def looped_check_update_should_finish():
            "checking until time to update flag and exit"
            while True:
                now = datetime.now()
                if now > should_finish_before:
                    nonlocal should_finish
                    should_finish = True
                    break
                await asyncio.sleep(0.1)

        async def finisher():
            "clean up + return. could also raise error"
            while True:
                if should_finish == True:
                    nonlocal browser, result
                    await browser.close()
                    return result
                await asyncio.sleep(0.1)

        # Event listener to capture and analyze fetch requests
        async def handle_request(request):
            url_of_interest = "https://lbkperp.lbank.com/cfd/agg/v1/sendQryAll"
            if request.url == url_of_interest:
                headers = request.headers

                nonlocal should_finish, result
                should_finish = True
                result = headers
                # should return result or error. for now only result or empty dict

        page.on("request", handle_request)

        # Open a webpage
        await page.goto("https://www.lbank.com/futures/btcusdt")

        # Start looper
        asyncio.create_task(looped_check_update_should_finish())

        return await finisher()


async def get_data_with_browser_headers_and_custom_requests() -> (
    GetDataWithBrowserHeadersAndCustomRequestsReturnType
):
    headers = await get_headers()

    all_symbols = get_all_symbols_headers(headers)

    semaphore = asyncio.Semaphore(2)

    with timeit_context("lbank scrape all"):
        tasks = [
            scrape_market_data_for_symbol(headers, symbol, semaphore)
            for symbol in all_symbols
        ]

        tasks_results = await asyncio.gather(*tasks)

    to_return: List[GetDataWithBrowserHeadersAndCustomRequestsReturnTypeElement] = [
        {"symbol": symbol, "data": task_result}
        for symbol, task_result in zip(all_symbols, tasks_results)
    ]

    return to_return


##
# WS
##


def ws_scrape_symbols_sequential(symbols: List[str]) -> List[WSScrapingResult]:
    scraping_results: List[WSScrapingResult] = []

    ws = create_connection("wss://lbkperpws.lbank.com/ws?version=1.0.0")
    for symbol in symbols:
        ws.send(
            '{"SendTopicAction":{"Action":"1","LocalNo":100,"TopicID":"7","FilterValue":"Exchange_%s","ResumeNo":-1}}'
            % symbol
        )
        for i in range(5):
            msg: WSMarketDataOverView = json.loads(
                ws.recv()
            )  # actually can be different type, next line chekcs it
            if (
                msg["action"] == "PushMarketDataOverView"
                and "requestNo" in msg
                and symbol == msg["result"][0]["data"]["InstrumentID"]
            ):
                scraping_results.append(
                    {
                        "symbol": symbol,
                        "data_point": msg["result"][0]["data"],
                    }
                )
                break
        else:
            print(f"oops.. symbol: {symbol}")
            scraping_results.append(
                {
                    "symbol": symbol,
                    "data_point": None,
                }
            )
        ws.send(
            '{"SendTopicAction":{"Action":"0","LocalNo":100,"TopicID":"7","FilterValue":"Exchange_%s","ResumeNo":-1}}'
            % symbol
        )

    return scraping_results


def ws_parallelized_sequential_scrape(all_pairs: List[str]):
    parallelization_limit = 10

    task_groups = split_list(all_pairs, parallelization_limit)

    with ThreadPoolExecutor(max_workers=parallelization_limit) as executor:
        # with ProcessPoolExecutor(max_workers=parallelization_limit) as executor:
        futures = [
            executor.submit(ws_scrape_symbols_sequential, task_group)
            for task_group in task_groups
        ]
        results = [future.result() for future in futures]

    results_flat = list(itertools.chain.from_iterable(results))

    return results_flat

    # with multiprocessing.Pool(parallelization_limit) as pool:
    #     results = pool.map(scrape_symbols_sequential, task_groups)
    # return results


def get_data_from_ws(all_symbols: List[str]):
    with timeit_context("lbank parallelized data from ws"):
        return ws_parallelized_sequential_scrape(all_symbols)


async def get_tickers_data() -> List[ScrapeResult]:
    all_symbols = await get_all_symbols()

    # qry_all_data_points_co = get_data_with_browser_headers_and_custom_requests() # login requires captcha, without login can't run requests of interest
    # data_from_ws_co = asyncio.to_thread(get_data_from_ws, all_symbols)

    # qry_all_data_points, data_from_ws = await asyncio.gather(
    #     qry_all_data_points_co, data_from_ws_co
    # )

    data_from_ws = await asyncio.to_thread(get_data_from_ws, all_symbols)

    to_return: List[ScrapeResult] = [
        {
            "symbol": symbol,
            "data_from_ws": [dp for dp in data_from_ws if dp["symbol"] == symbol][0],
        }
        for symbol in all_symbols
    ]
    return to_return

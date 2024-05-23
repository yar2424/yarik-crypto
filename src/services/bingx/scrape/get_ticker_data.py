import asyncio
from datetime import datetime, timedelta

import httpx
from playwright.async_api import async_playwright
from typing_extensions import List, cast

from src.services.bingx.types_ import ApiResponse, Contract
from src.services.mexc.types_ import Ticker, TickersResponse


def get_tickers_data_direct() -> List[Contract]:
    "requires population of headers for request to work. some of the headers expire - hence need to pretend to be browser (dynamically execute js to keep requests (headers) fresh). still, headers are valid for substential amount of time."
    url = "https://api-swap.qq-os.com/api/v1/quote/all/contracts/get?tradingUnit=COIN"
    headers = {}
    response = httpx.get(url, headers=headers)
    data: ApiResponse = response.json()
    return data["data"]["contracts"]


async def get_tickers_data() -> List[Contract]:
    async def scrape() -> ApiResponse:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            should_finish_before = datetime.now() + timedelta(seconds=10)  # for timeout
            should_finish = False  # flip when time to finish (timeout)
            result: ApiResponse = cast(
                ApiResponse, {}
            )  # request response data will be stored here

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
                if (
                    request.url
                    == "https://api-swap.qq-os.com/api/v1/quote/all/contracts/get?tradingUnit=COIN"
                ):
                    response = await request.response()
                    body = await response.json()
                    nonlocal should_finish, result
                    should_finish = True
                    result = body
                    # should return result or error. for now only result of empty dict

            page.on("requestfinished", handle_request)

            # Open a webpage
            await page.goto("https://swap.bingx.com/en/BTC-USDT")

            # Start looper
            asyncio.create_task(looped_check_update_should_finish())

            return await finisher()

    data = await scrape()
    if not data or "data" not in data:
        print("oops")
        print(data)
        print(dir(data))
        print(data.keys())
    return data["data"]["contracts"]


def get_ticker_of_interest(tickers: List[Contract], symbol: str):
    for ticker in tickers:
        if ticker["symbol"] == symbol:
            return ticker

    raise ValueError(f"Ticker with symbol '{symbol}' was not found")


async def get_ticker_data(symbol: str) -> Contract:
    tickers = await get_tickers_data()
    ticker = get_ticker_of_interest(tickers, symbol)
    return ticker

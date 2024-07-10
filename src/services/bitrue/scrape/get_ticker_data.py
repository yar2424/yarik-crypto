import asyncio
import itertools
import json
import os
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import httpx
import playwright.async_api
from playwright.async_api import async_playwright
from typing_extensions import List, Optional, Tuple, TypedDict, cast
from websocket import create_connection

from src.services.bitrue.scrape.types_.public_info_req import PublicInfoApiResponse
from src.services.bitrue.scrape.types_.public_market_info_req import (
    PublicMarketInfoApiResponse,
    PublicMarketInfoApiResponseWithId,
)
from src.services.bitrue.scrape.types_.reqs_params import ReqInfo, ReqsInfo
from src.services.bitrue.scrape.types_.types_ import ScrapeResult
from src.services.bitrue.scrape.types_.ws_data import WSMessage, WSScrapeResult
from src.utils.utils import split_list, timeit_context, ungzip_bytes_to_text


class SymbolAndId(TypedDict):
    symbol: str
    id: int


async def get_all_symbols() -> List[SymbolAndId]:
    reqs_params = await get_reqs_params()
    public_info = await make_public_info_req(reqs_params["public_info"])
    to_return: List[SymbolAndId] = [
        {"symbol": contract["symbol"], "id": contract["id"]}
        for contract in public_info["data"]["contractList"]
        if contract["symbol"].endswith(
            "USDT"
        )  # there is more but i am interested only in usdt (there is also usd)
    ]
    return sorted(to_return, key=lambda x: x["id"])


##
# WS
##


def get_ws_info() -> WSMessage:
    ws = create_connection("wss://futuresws.bitrue.com/kline-api/ws")
    out_msg = '{"event":"req","params":{"channel":"review"}}'
    ws.send(out_msg)

    msg: WSMessage = json.loads(ungzip_bytes_to_text(ws.recv()))

    return msg


def scrape_ws_closing_price_with_proper_symbols(
    symbols: List[SymbolAndId],
) -> List[WSScrapeResult]:
    ws_info = get_ws_info()

    ws_info_proper_symbols = {
        standardise_ws_symbol(key): value for key, value in ws_info["data"].items()
    }

    result: List[WSScrapeResult] = [
        {
            "symbol": symbol_and_id["symbol"],
            "symbol_id": symbol_and_id["id"],
            "close": float(ws_info_proper_symbols[symbol_and_id["symbol"]]["close"]),
        }
        for symbol_and_id in symbols
    ]

    return result


def standardise_ws_symbol(ws_symbol: str):
    # turn ws symbol into expected format: 'e_btcusdt' -> 'BTC-USDT
    ws_symbol_ = ws_symbol[2:]  # 'e_btcusdt' -> 'btcusdt'
    ws_symbol_ = ws_symbol_[:-4] + "-" + ws_symbol_[-4:]  # 'btcusdt' -> 'btc-usdt'
    ws_symbol_ = ws_symbol_.upper()  # 'btc-usdt' -> 'BTC-USDT

    return ws_symbol_


##
# Browser
##


async def get_reqs_params() -> ReqsInfo:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        should_finish_before = datetime.now() + timedelta(seconds=10)  # for timeout
        should_finish = False  # flip when time to finish (timeout)
        result: ReqsInfo = {}  # type: ignore # request response data will be stored here

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
            urls_of_interest = {
                "public_info": "https://futures.bitrue.com/fe-co-api/common/public_info",
                "public_market_info": "https://futures.bitrue.com/fe-co-api/common/public_market_info",
            }
            nonlocal result
            if request.url.startswith(urls_of_interest["public_info"]):
                parsed_url = urllib.parse.urlparse(request.url)
                query_params = urllib.parse.parse_qs(parsed_url.query)
                headers = request.headers
                post_data_str = request.post_data_buffer.decode("utf-8")
                body_params = json.loads(post_data_str)

                result.update(
                    {
                        "public_info": {
                            "headers": headers,
                            "query_params": query_params,  # type: ignore
                            "body_params": body_params,
                            "url": urls_of_interest["public_info"],
                        }
                    }
                )  # type: ignore
                # should return result or error. for now only result or empty dict
            if request.url.startswith(urls_of_interest["public_market_info"]):
                parsed_url = urllib.parse.urlparse(request.url)
                query_params = urllib.parse.parse_qs(parsed_url.query)
                headers = request.headers

                post_data_str = request.post_data_buffer.decode("utf-8")
                body_params = json.loads(post_data_str)

                result.update(
                    {
                        "public_market_info": {
                            "headers": headers,
                            "query_params": query_params,  # type: ignore
                            "body_params": body_params,
                            "url": urls_of_interest["public_market_info"],
                        }
                    }
                )  # type: ignore

            nonlocal should_finish
            # all required keys in result dict were populated
            all_keys_populated = all(
                [required_key in result for required_key in urls_of_interest]
            )
            if all_keys_populated:
                should_finish = True

        page.on("request", handle_request)

        # Open a webpage
        await page.goto("https://www.bitrue.com/futures/BTC")

        # Start looper
        asyncio.create_task(looped_check_update_should_finish())

        return await finisher()


async def make_public_info_req(req_info: ReqInfo) -> PublicInfoApiResponse:
    url = req_info["url"]
    headers = req_info["headers"]
    params = {k: v[0] for k, v in req_info["query_params"].items()}  # type: ignore
    body = req_info["body_params"]

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, params=params, json=body)  # type: ignore
        response.raise_for_status()
        return response.json()


async def make_public_market_info_req(
    symbol_id: int, req_info: ReqInfo
) -> PublicMarketInfoApiResponseWithId:
    url = req_info["url"]
    headers = req_info["headers"]
    params = {k: v[0] for k, v in req_info["query_params"].items()}  # type: ignore
    body = req_info["body_params"]

    body["contractId"] = symbol_id

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, params=params, json=body)  # type: ignore
        response.raise_for_status()

    response_json: PublicMarketInfoApiResponse = response.json()

    to_return: PublicMarketInfoApiResponseWithId = {**response_json, "id": symbol_id}

    return to_return


async def scrape_public_market_info_for_symbols(
    symbols: List[SymbolAndId],
) -> List[PublicMarketInfoApiResponseWithId]:
    reqs_params = await get_reqs_params()

    max_concurrent_requests = 20
    semaphore = asyncio.Semaphore(max_concurrent_requests)

    async def fetch_info(symbol: SymbolAndId):
        async with semaphore:
            symbol_id = symbol["id"]
            return await make_public_market_info_req(
                symbol_id, reqs_params["public_market_info"]
            )

    tasks = [fetch_info(symbol) for symbol in symbols]
    results = await asyncio.gather(*tasks)
    return results


async def get_tickers_data() -> List[ScrapeResult]:
    all_symbols = await get_all_symbols()

    reqs_params = await get_reqs_params()

    public_info = await make_public_info_req(reqs_params["public_info"])
    public_market_info = await scrape_public_market_info_for_symbols(all_symbols)

    ws_info = scrape_ws_closing_price_with_proper_symbols(all_symbols)

    # reconcile
    to_return: List[ScrapeResult] = [
        {
            "id": symbol["id"],
            "symbol": symbol["symbol"],
            "public_info": [
                contract
                for contract in public_info["data"]["contractList"]
                if contract["id"] == symbol["id"]
            ][0],
            "public_market_info": [
                pmi for pmi in public_market_info if pmi["id"] == symbol["id"]
            ][0],
            "ws_info": [wsi for wsi in ws_info if wsi["symbol_id"] == symbol["id"]][0],
        }
        for symbol in all_symbols
    ]
    return to_return

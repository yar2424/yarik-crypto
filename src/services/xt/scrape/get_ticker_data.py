import asyncio
import itertools
import json
import os
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import httpx
import playwright.async_api
from playwright.async_api import async_playwright
from typing_extensions import List, Optional, Tuple, cast
from websocket import create_connection

from src.services.xt.types_ import (FundingRateAPIResponse,
                                    IndexPriceAPIResponse,
                                    IndexPriceResultEntry,
                                    MarkPriceAPIResponse, MarkPriceResultEntry,
                                    ScrapeResult, TickersDataAPIResponse,
                                    TickersDataResultEntry)
from src.utils.utils import split_list, timeit_context

##
# WS
##


def get_all_symbols() -> List[str]:
    res = httpx.get("https://www.xt.com/fapi/market/v1/public/q/tickers")
    data: TickersDataAPIResponse = res.json()

    symbols = [d["s"] for d in data["result"] if d["s"].endswith("_usdt")]

    return sorted(symbols)


def scrape_mark_prices(symbols: List[str]) -> List[MarkPriceResultEntry]:
    res = httpx.get("https://www.xt.com/fapi/market/v1/public/q/mark-price")
    data_: MarkPriceAPIResponse = res.json()
    data = data_["result"]

    # filter out (response contains rogue pairs)
    filtered_out: List[MarkPriceResultEntry] = [dp for dp in data if dp["s"] in symbols]
    return filtered_out


def scrape_index_prices(symbols: List[str]) -> List[IndexPriceResultEntry]:
    res = httpx.get("https://www.xt.com/fapi/market/v1/public/q/index-price")
    data_: IndexPriceAPIResponse = res.json()
    data = data_["result"]

    # filter out (response contains rogue pairs)
    filtered_out: List[IndexPriceResultEntry] = [
        dp for dp in data if dp["s"] in symbols
    ]
    return filtered_out


def scrape_tickers_data(symbols: List[str]) -> List[TickersDataResultEntry]:
    res = httpx.get("https://www.xt.com/fapi/market/v1/public/q/tickers")
    data_: TickersDataAPIResponse = res.json()
    data = data_["result"]

    # filter out (response contains rogue pairs)
    filtered_out: List[TickersDataResultEntry] = [
        dp for dp in data if dp["s"] in symbols
    ]
    return filtered_out


async def scrape_single_funding_rate(
    symbol: str, sempahore: asyncio.Semaphore
) -> FundingRateAPIResponse:
    async with sempahore:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                f"https://www.xt.com/fapi/market/v1/public/q/funding-rate?symbol={symbol}"
            )
        data: FundingRateAPIResponse = res.json()
        return data


async def scrape_funding_rates(symbols: List[str]) -> List[FundingRateAPIResponse]:
    semaphore = asyncio.Semaphore(40)
    tasks = [scrape_single_funding_rate(symbol, semaphore) for symbol in symbols]

    results = await asyncio.gather(*tasks)

    return results


async def get_tickers_data() -> List[ScrapeResult]:
    symbols = get_all_symbols()

    mark_prices = scrape_mark_prices(symbols)
    index_prices = scrape_index_prices(symbols)
    tickers_price_data = scrape_tickers_data(symbols)
    funding_rates = await scrape_funding_rates(symbols)

    to_return: List[ScrapeResult] = []

    # for symbol in symbols:
    #     try:
    #         mark_price = [
    #             mark_price for mark_price in mark_prices if mark_price["s"] == symbol
    #         ][0]["p"]
    #     except IndexError:
    #         mark_price = None

    #     try:
    #         index_price = [
    #             index_price
    #             for index_price in index_prices
    #             if index_price["s"] == symbol
    #         ][0]["p"]
    #     except IndexError:
    #         index_price = None

    #     try:
    #         last_price = [dp for dp in tickers_price_data if dp["s"] == symbol][0]["c"]
    #     except IndexError:
    #         last_price = None

    #     try:
    #         funding_rate = [
    #             funding_rate
    #             for funding_rate in funding_rates
    #             if funding_rate["result"]["symbol"] == symbol
    #         ][0]["result"]["fundingRate"]
    #     except IndexError:
    #         funding_rate = 1_000_000

    #     symbol_scrape_result: ScrapeResult = {
    #         "symbol": symbol,
    #         "mark_price": mark_price,
    #         "index_price": index_price,
    #         "last_price": last_price,
    #         "funding_rate": funding_rate,
    #     }

    #     to_return.append(symbol_scrape_result)

    to_return: List[ScrapeResult] = [
        {
            "symbol": symbol,
            "mark_price": float(
                [mark_price for mark_price in mark_prices if mark_price["s"] == symbol][
                    0
                ]["p"]
            ),
            "index_price": float(
                [
                    index_price
                    for index_price in index_prices
                    if index_price["s"] == symbol
                ][0]["p"]
            ),
            "last_price": float(
                [dp for dp in tickers_price_data if dp["s"] == symbol][0]["c"]
            ),
            "funding_rate": [
                funding_rate
                for funding_rate in funding_rates
                if funding_rate["result"]["symbol"] == symbol
            ][0]["result"]["fundingRate"]
            or 1_000_000,
        }
        for symbol in symbols
    ]
    return to_return

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

from src.services.websea.scrape.types_.symbol_detail_req import (
    SymbolDetailApiResponse,
    SymbolDetailResult,
)
from src.services.websea.scrape.types_.symbol_list import (
    SymbolListApiResponse,
    SymbolListResultItem,
)
from src.services.websea.scrape.types_.types_ import ScrapeResult
from src.utils.utils import split_list, timeit_context


def get_all_symbols() -> List[str]:
    "Symbol format: BTC-USDT"
    symbol_list_data = get_symbol_list_req()

    all_symbols = [data["name"] for data in symbol_list_data]

    return sorted(all_symbols)


##
# Reqs
##


def get_symbol_list_req() -> List[SymbolListResultItem]:
    symbol_list_response: SymbolListApiResponse = httpx.get(
        "https://capi.websea.com/webApi/symbol/list"
    ).json()
    return symbol_list_response["result"]


def get_symbol_detail_req(symbol: str) -> SymbolDetailResult:
    try:
        url = f"https://capi.websea.com/webApi/market/getSymbolDetail?symbol={symbol}"
        response: SymbolDetailApiResponse = httpx.get(url).json()
    except Exception as e:
        print(symbol)
    return response["result"]


def get_symbol_detail_req_sequential(
    symbols: List[str],
) -> List[SymbolDetailResult]:
    return [get_symbol_detail_req(s) for s in symbols]


def parallelized_scrape_symbol_detail_req(
    symbols: List[str],
) -> List[SymbolDetailResult]:
    parallelization_limit = 8

    task_groups = split_list(symbols, parallelization_limit)

    with ThreadPoolExecutor(max_workers=parallelization_limit) as executor:
        futures = [
            executor.submit(get_symbol_detail_req_sequential, task_group)
            for task_group in task_groups
        ]
        results = [future.result() for future in futures]

    results_flat = list(itertools.chain.from_iterable(results))

    return results_flat


async def get_tickers_data() -> List[ScrapeResult]:
    all_symbols = get_all_symbols()

    symbol_list_data = get_symbol_list_req()

    symbols_details = parallelized_scrape_symbol_detail_req(all_symbols)

    # reconcile
    to_return: List[ScrapeResult] = [
        {
            "symbol": symbol,
            "symbol_list_data": [
                data for data in symbol_list_data if data["name"] == symbol
            ][0],
            "symbol_detail": [
                data for data in symbols_details if data["symbolName"] == symbol
            ][0],
        }
        for symbol in all_symbols
    ]

    return to_return

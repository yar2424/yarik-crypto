import asyncio
import itertools
import json
import os
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import httpx
import playwright.async_api
import pytest
from playwright.async_api import async_playwright
from typing_extensions import List, Optional, Tuple, TypedDict, cast
from websocket import create_connection

from src.services.bitrue.scrape.get_ticker_data import (
    get_all_symbols,
    get_reqs_params,
    get_tickers_data,
    get_ws_info,
    make_public_info_req,
    make_public_market_info_req,
    scrape_public_market_info_for_symbols,
    scrape_ws_closing_price_with_proper_symbols,
)
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


def test_get_ws_info():
    result = get_ws_info()
    print()


@pytest.mark.debug_test
@pytest.mark.asyncio
async def test_scrape_ws_closing_price_with_proper_symbols():
    all_symbols = await get_all_symbols()
    result = scrape_ws_closing_price_with_proper_symbols(all_symbols)
    print()


##
# Browser
##


@pytest.mark.asyncio
async def test_get_reqs_params():
    result = await get_reqs_params()
    print(result)


@pytest.mark.asyncio
async def test_make_public_info_req():
    reqs_params = await get_reqs_params()
    result = await make_public_info_req(reqs_params["public_info"])
    print(result.keys())
    print(str(result)[:3000])


@pytest.mark.asyncio
async def test_get_all_symbols():
    result = await get_all_symbols()
    print(result)


@pytest.mark.asyncio
async def test_make_public_market_info_req():
    reqs_params = await get_reqs_params()
    result = await make_public_market_info_req(1, reqs_params["public_market_info"])
    print(result)


@pytest.mark.asyncio
async def test_scrape_public_market_info_for_symbols():
    all_symbols = await get_all_symbols()
    with timeit_context("20 parallel"):
        result = await scrape_public_market_info_for_symbols(all_symbols)
    # print(result)


@pytest.mark.asyncio
async def test_get_tickers_data():
    with timeit_context("get tickers data"):
        result = await get_tickers_data()
    print(str(result)[:3000])

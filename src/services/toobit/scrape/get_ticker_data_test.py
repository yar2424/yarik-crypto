import asyncio
import itertools
import json
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import httpx
import playwright.async_api
import pytest
from playwright.async_api import async_playwright
from typing_extensions import List, Optional, Tuple, cast
from websocket import create_connection

from src.services.toobit.scrape.get_ticker_data import (
    get_all_symbols,
    get_funding_rates_req,
    get_futures_req,
    get_tickers_data,
    get_ws_index_price,
    get_ws_mark_price,
    get_ws_slow_broker,
)
from src.utils.utils import split_list, timeit_context

##
# WS
##


def test_get_ws_slow_broker():
    get_ws_slow_broker()


def test_get_futures_req():
    get_futures_req()


def test_get_funding_rates_req():
    get_funding_rates_req()


def test_get_all_pairs():
    get_all_symbols()


def test_get_ws_mark_price():
    res = get_ws_mark_price("BTC-SWAP-USDT")
    print()


def test_get_ws_index_price():
    res = get_ws_index_price("BTC-SWAP-USDT")
    print()


@pytest.mark.debug_test
@pytest.mark.asyncio
async def test_get_tickers_data():
    with timeit_context():
        res = await get_tickers_data()
    print()

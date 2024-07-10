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

from src.services.websea.scrape.get_ticker_data import (
    get_symbol_detail_req,
    get_tickers_data,
)
from src.utils.utils import split_list, timeit_context


def test_get_symbol_detail_req():
    result = get_symbol_detail_req("BTC-USDT")
    print()


@pytest.mark.debug_test
@pytest.mark.asyncio
async def test_get_tickers_data():
    with timeit_context():
        result = await get_tickers_data()
    print()

import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from datetime import datetime, timedelta

import httpx
import playwright
import playwright.async_api
import pytest
from playwright.async_api import async_playwright
from typing_extensions import List, cast

from src.services.bingx.types_ import ApiResponse, Contract
from src.services.bitvenus.scrape.get_ticker_data import get_tickers_data
from src.services.bitvenus.types_ import ScrapingResult
from src.utils.utils import split_list, timeit_context


@pytest.mark.debug_test
@pytest.mark.asyncio
async def test_get_tickers_data():
    with timeit_context():
        res = await get_tickers_data()
    print()

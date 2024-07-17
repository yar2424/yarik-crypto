import asyncio
import itertools
import json
import os
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import httpx
import playwright.async_api
import pytest
from playwright.async_api import async_playwright
from typing_extensions import List, Optional, Tuple, cast
from websocket import create_connection

from src.services.xt.scrape.get_ticker_data import get_tickers_data
from src.services.xt.types_ import (
    FundingRateAPIResponse,
    IndexPriceAPIResponse,
    IndexPriceResultEntry,
    MarkPriceAPIResponse,
    MarkPriceResultEntry,
    ScrapeResult,
    TickersDataAPIResponse,
    TickersDataResultEntry,
)
from src.utils.utils import split_list, timeit_context


@pytest.mark.debug_test
@pytest.mark.asyncio
async def test_get_tickers_data():
    result = await get_tickers_data()
    print()

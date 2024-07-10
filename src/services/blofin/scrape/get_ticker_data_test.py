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

from src.services.blofin.scrape.get_ticker_data import (
    get_basic_contract_info_for_symbol_req,
    get_index_all_ws,
    get_ticker_everview_ws,
    get_tickers_data,
)
from src.utils.utils import split_list, timeit_context

##
# WS
##


def test_get_index_all_ws():
    get_index_all_ws()


def test_get_ticker_everview_ws():
    get_ticker_everview_ws()


@pytest.mark.debug_test
@pytest.mark.asyncio
async def test_get_tickers_data():
    with timeit_context():
        result = await get_tickers_data()
    print()

import asyncio
import itertools
import json
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import httpx
import playwright.async_api
from playwright.async_api import async_playwright
from typing_extensions import List, Optional, Tuple, cast
from websocket import create_connection

from src.services.phemex.types_ import MarketData, ScrapeResult, WSMarketDataMsg
from src.utils.utils import split_list, timeit_context

##
# WS
##


def market_data_dict_data_point_to_proper_type(
    market_data_dict_data_point: List[str],
) -> MarketData:
    return {
        "symbol": str(market_data_dict_data_point[0]),
        "openRp": float(market_data_dict_data_point[1]),
        "highRp": float(market_data_dict_data_point[2]),
        "lowRp": float(market_data_dict_data_point[3]),
        "lastRp": float(market_data_dict_data_point[4]),
        "volumeRq": float(market_data_dict_data_point[5]),
        "turnoverRv": float(market_data_dict_data_point[6]),
        "openInterestRv": float(market_data_dict_data_point[7]),
        "indexRp": float(market_data_dict_data_point[8]),
        "markRp": float(market_data_dict_data_point[9]),
        "fundingRateRr": float(market_data_dict_data_point[10]),
        "predFundingRateRr": float(market_data_dict_data_point[11]),
    }


def get_all_symbols() -> List[str]:
    ws = create_connection("wss://ws10.phemex.com/")
    ws.send('{"method":"perp_market24h_pack_p.subscribe","params":{},"id":2}')
    ws.recv()
    msg: WSMarketDataMsg = json.loads(ws.recv())
    ws.close()

    data = msg["data"]
    proper_data = [market_data_dict_data_point_to_proper_type(d) for d in data]

    symbols = [d["symbol"] for d in proper_data]

    return sorted(symbols)


def ws_market_data_scrape() -> List[MarketData]:
    ws = create_connection("wss://ws10.phemex.com/")
    ws.send('{"method":"perp_market24h_pack_p.subscribe","params":{},"id":2}')
    ws.recv()
    msg: WSMarketDataMsg = json.loads(ws.recv())
    ws.close()

    data = msg["data"]
    proper_data = [market_data_dict_data_point_to_proper_type(d) for d in data]

    return proper_data


async def get_tickers_data() -> List[ScrapeResult]:
    market_data = ws_market_data_scrape()
    scrape_results: List[ScrapeResult] = [
        {"symbol": d["symbol"], "market_data": d} for d in market_data
    ]
    return scrape_results

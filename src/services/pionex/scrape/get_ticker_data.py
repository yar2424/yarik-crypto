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

from src.services.pionex.types_ import (DataEntry, DataEntryProperTypes,
                                        FutureIndexesData, IndexDataEntry,
                                        IndexDataEntryProperTypes,
                                        ScrapeResult, TickersPriceData)
from src.utils.utils import split_list, timeit_context

##
# WS
##


def get_all_symbols() -> List[str]:
    ws = create_connection("wss://stream.pionex.com/stream/v2")
    ws.send(
        '{"action":"subscribe","channel":"tickers.price","data":[{"exchange":"pionex.v2"},{"exchange":"pionex.v2","quote":"USDT"}]}'  # all_symbols, last_price
    )
    msg: TickersPriceData = json.loads(ws.recv())
    data = msg["data"]
    symbols_of_interest = [
        d["b"] for d in data if d["b"].endswith(".PERP") and d["q"] == "USDT"
    ]
    ws.close()
    return sorted(symbols_of_interest)


def ws_scrape_tickers_price_data() -> List[DataEntryProperTypes]:
    ws = create_connection("wss://stream.pionex.com/stream/v2")
    ws.send(
        '{"action":"subscribe","channel":"tickers.price","data":[{"exchange":"pionex.v2"},{"exchange":"pionex.v2","quote":"USDT"}]}'  # all_symbols, last_price
    )
    msg: TickersPriceData = json.loads(ws.recv())
    ws.close()

    data = msg["data"]
    data_points_of_interest = [d for d in data if d["b"].endswith(".PERP")  and d["q"] == "USDT"]
    data_points_of_interest_sorted = sorted(
        data_points_of_interest, key=lambda v: v["b"]
    )
    data_points_of_interest_converted: List[DataEntryProperTypes] = [
        {
            "e": d["e"],
            "b": d["b"],
            "q": d["q"],
            "p": float(d["p"]),
            "h": float(d["h"]),
            "l": float(d["l"]),
            "c": float(d["c"]),
            "f": d["f"],
            "v": float(d["v"]),
            "w": float(d["w"]),
            "u": float(d["u"]),
            "tc": d["tc"],
            "n": d["n"],
        }
        for d in data_points_of_interest_sorted
    ]
    return data_points_of_interest_converted


def ws_scrape_futures_indexes_data(
    symbols_of_interest: List[str],
) -> List[IndexDataEntryProperTypes]:
    ws = create_connection("wss://stream.pionex.com/stream/v2")
    ws.send(
        '{"action":"subscribe","channel":"future.indexes","data":[{"exchange":"pionex.v2"}]}'
    )
    msg: FutureIndexesData = json.loads(ws.recv())
    ws.close()

    data = msg["data"]
    data_points_of_interest = [
        d for d in data if d["b"] in symbols_of_interest and d["q"] == "USDT"
    ]
    data_points_of_interest_sorted = sorted(
        data_points_of_interest, key=lambda v: v["b"]
    )
    data_points_of_interest_converted: List[IndexDataEntryProperTypes] = [
        {
            "e": d["e"],
            "b": d["b"],
            "q": d["q"],
            "ip": float(d["ip"]),
            "mp": float(d["mp"]),
            "im": float(d["im"]),
            "nfr": float(d["nfr"]),
            "nft": d["nft"],
            "t": d["t"],
            "s": d["s"],
        }
        for d in data_points_of_interest_sorted
    ]
    return data_points_of_interest_converted


async def get_tickers_data() -> List[ScrapeResult]:
    symbols = get_all_symbols()

    tickers_price_data = ws_scrape_tickers_price_data()
    futures_indexes_data = ws_scrape_futures_indexes_data(symbols)

    to_return: List[ScrapeResult] = [
        {
            "symbol": symbol,
            "tickers_price_data": [
                dp for dp in tickers_price_data if dp["b"] == symbol
            ][0],
            "futures_indexes_data": [
                dp for dp in futures_indexes_data if dp["b"] == symbol
            ][0],
        }
        for symbol in symbols
    ]
    return to_return

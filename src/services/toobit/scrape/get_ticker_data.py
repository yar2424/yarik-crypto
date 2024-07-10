import asyncio
import itertools
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import httpx
import playwright.async_api
from playwright.async_api import async_playwright
from typing_extensions import List, Optional, Tuple, cast
from websocket import create_connection

from src.services.toobit.scrape.types_.funding_rates_req import (
    FundingRatesReqResponseItem,
)
from src.services.toobit.scrape.types_.futures_req import FuturesReqResponse
from src.services.toobit.scrape.types_.types_ import ScrapeResult
from src.services.toobit.scrape.types_.ws_index_price import IndexPriceMessage
from src.services.toobit.scrape.types_.ws_mark_price import MarkPriceMessage
from src.services.toobit.scrape.types_.ws_slow_broker import SlowBrokerMessage
from src.utils.utils import split_list, timeit_context, ungzip_bytes_to_text


def get_all_symbols():
    "symbol format: BTC-SWAP-USDT"

    # res1 = get_ws_slow_broker()
    res2 = get_futures_req()
    # res3 = get_funding_rates_req()

    # data1 = res1["data"]
    data2 = res2["data"]["futuresSymbol"]
    # data3 = res3

    # pairs1 = [dp["s"] for dp in data1 if "-SWAP-" in dp["s"]]
    pairs2 = [dp["symbolId"] for dp in data2]
    # pairs3 = [dp["tokenId"] for dp in data3]

    # pairs = set(pairs1).intersection(set(pairs2)).intersection(set(pairs3))

    pairs = pairs2

    return sorted(pairs)


##
# WS
##


def get_ws_slow_broker() -> SlowBrokerMessage:
    # ws = create_connection("wss://ws10.toobit.com/")
    ws = create_connection("wss://bws.toobit.com/ws/quote/v1?lang=en-us")
    ws.send(
        '{"event":"sub","id":"slowBroker","topic":"slowBroker","params":{"reduceSerial":true,"realtimeInterval":"24h"}}'
    )
    msg: SlowBrokerMessage = json.loads(ws.recv())
    ws.close()

    return msg


def get_ws_mark_price(symbol: str) -> MarkPriceMessage:
    ws = create_connection("wss://bws.toobit.com/ws/quote/v1?lang=en-us")
    out_msg = (
        '{"id":"markPrice","topic":"markPrice","event":"sub","symbol":"%s","params":{"reduceSerial":true,"binary":true,"limit":1500}}'
        % symbol
    )
    ws.send(out_msg)
    msg: MarkPriceMessage = json.loads(ungzip_bytes_to_text(ws.recv()))
    ws.close()

    return msg


def get_ws_mark_prices_sequential(symbols: List[str]) -> List[MarkPriceMessage]:
    return [get_ws_mark_price(s) for s in symbols]


def parallelized_scrape_ws_mark_price(symbols: List[str]):
    parallelization_limit = 10

    task_groups = split_list(symbols, parallelization_limit)

    with ThreadPoolExecutor(max_workers=parallelization_limit) as executor:
        futures = [
            executor.submit(get_ws_mark_prices_sequential, task_group)
            for task_group in task_groups
        ]
        results = [future.result() for future in futures]

    results_flat = list(itertools.chain.from_iterable(results))

    return results_flat


def get_ws_index_price(symbol: str) -> IndexPriceMessage:
    ws = create_connection("wss://bws.toobit.com/ws/quote/v1?lang=en-us")
    symbol_ = symbol.replace("-SWAP-", "")  # "BTC-SWAP-USDT" -> "BTCUSDT"
    symbol_ = symbol_.replace("1000", "")  # "1000FLOKIUSDT" -> "FLOKIUSDT"
    symbol_ = symbol_.replace("ID2", "ID")  # "ID2USDT" -> "IDUSDT"
    out_msg = (
        '{"id":"index","topic":"index","event":"sub","symbol":"%s","params":{"reduceSerial":true,"binary":true,"limit":1500}}'
        % symbol_
    )
    ws.send(out_msg)

    msg: IndexPriceMessage = json.loads(ungzip_bytes_to_text(ws.recv()))

    ws.close()

    msg["symbol"] = symbol  # "BTCUSDT" -> "BTC-SWAP-USDT"

    return msg


def get_ws_index_prices_sequential(symbols: List[str]) -> List[IndexPriceMessage]:
    return [get_ws_index_price(s) for s in symbols]


def parallelized_scrape_ws_index_price(symbols: List[str]):
    parallelization_limit = 10

    task_groups = split_list(symbols, parallelization_limit)

    with ThreadPoolExecutor(max_workers=parallelization_limit) as executor:
        futures = [
            executor.submit(get_ws_index_prices_sequential, task_group)
            for task_group in task_groups
        ]
        results = [future.result() for future in futures]

    results_flat = list(itertools.chain.from_iterable(results))

    return results_flat


##
# Reqs
##


def get_futures_req() -> FuturesReqResponse:
    res = httpx.get(
        "https://bapi.toobit.com/bapi/v2/basic/symbol/futures?r=msi6jeadgr8&__test__=https:%2F%2Fwww.toobit.com%2Fen-US%2Ffutures%2FBTC-SWAP-USDT"
    )
    data: FuturesReqResponse = res.json()
    return data


def get_funding_rates_req() -> List[FundingRatesReqResponseItem]:
    res = httpx.get(
        "https://bapi.toobit.com/bapi/v1/futures/funding_rates?r=5u5stocbdtg&__test__=https:%2F%2Fwww.toobit.com%2Fen-US%2Ffutures%2FBTC-SWAP-USDT"
    )
    data: List[FundingRatesReqResponseItem] = res.json()
    return data


async def get_tickers_data() -> List[ScrapeResult]:
    all_symbols = get_all_symbols()

    with ThreadPoolExecutor(max_workers=1000) as executor:
        # Create futures for each function call
        future_slow_broker = executor.submit(get_ws_slow_broker)
        future_index_prices = executor.submit(
            parallelized_scrape_ws_index_price, all_symbols
        )
        future_mark_prices = executor.submit(
            parallelized_scrape_ws_mark_price, all_symbols
        )
        future_futures = executor.submit(get_futures_req)
        future_funding_rates = executor.submit(get_funding_rates_req)

        # Collect results from futures
        slow_broker = future_slow_broker.result()
        index_prices = future_index_prices.result()
        mark_prices = future_mark_prices.result()
        futures = future_futures.result()
        funding_rates = future_funding_rates.result()

    # reconcile
    to_return: List[ScrapeResult] = [
        {
            "symbol": symbol,
            "slow_broker": [
                data for data in slow_broker["data"] if data["s"] == symbol
            ][0],
            "index_price": [data for data in index_prices if data["symbol"] == symbol][
                0
            ],
            "mark_price": [data for data in mark_prices if data["symbol"] == symbol][0],
            "futures": [
                data
                for data in futures["data"]["futuresSymbol"]
                if data["symbolId"] == symbol
            ][0],
            "funding_rate": [
                data for data in funding_rates if data["tokenId"] == symbol
            ][0],
        }
        for symbol in all_symbols
    ]
    return to_return

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

from src.services.blofin.scrape.types_.basic_contract_info_req import (
    BasicContractInfoApiResponse,
)
from src.services.blofin.scrape.types_.index_all_ws import IndexAllMessage
from src.services.blofin.scrape.types_.ticker_overview_ws import TickerOverviewMessage
from src.services.blofin.scrape.types_.types_ import ScrapeResult
from src.utils.utils import split_list, timeit_context


def get_all_symbols():
    "Symbol format: BTC-USDT"
    index_all = get_index_all_ws()
    all_symbols = [data["symbol"] for data in index_all["instruments"]]

    return sorted(all_symbols)


##
# WS
##


def get_index_all_ws() -> IndexAllMessage:
    ws = create_connection("wss://ws-public.blofin.com/websocket")
    out_msg = '{"op":"SUBSCRIBE","args":[{"channel":"INDEX-ALL","symbol":"ALL","update_speed":"3000ms"}],"id":6}'
    ws.send(out_msg)

    ws.recv()  # subscription confirmation
    msg: IndexAllMessage = json.loads(ws.recv())

    ws.close()

    return msg


def get_ticker_everview_ws() -> TickerOverviewMessage:
    ws = create_connection("wss://ws-public.blofin.com/websocket")
    out_msg = '{"op":"SUBSCRIBE","args":[{"channel":"TICKER-OVERVIEW","symbol":"ALL"}],"id":7}'
    ws.send(out_msg)

    ws.recv()  # subscription confirmation
    msg: TickerOverviewMessage = json.loads(ws.recv())

    ws.close()

    return msg


##
# Reqs
##


def get_basic_contract_info_for_symbol_req(symbol: str) -> BasicContractInfoApiResponse:
    try:
        url = f"https://blofin.com/uapi/v1/basic/contract/info?symbol={symbol}"
        result: BasicContractInfoApiResponse = httpx.get(url).json()
    except Exception as e:
        print(symbol)
    return result


# def get_basic_contract_info_for_symbol_reqs_sequential(
#     symbols: List[str],
# ) -> List[BasicContractInfoApiResponse]:
#     return [get_basic_contract_info_for_symbol_req(s) for s in symbols]


# def parallelized_scrape_basic_contract_info_req(
#     symbols: List[str],
# ) -> List[BasicContractInfoApiResponse]:
#     parallelization_limit = 2

#     task_groups = split_list(symbols, parallelization_limit)

#     with ThreadPoolExecutor(max_workers=parallelization_limit) as executor:
#         futures = [
#             executor.submit(
#                 get_basic_contract_info_for_symbol_reqs_sequential, task_group
#             )
#             for task_group in task_groups
#         ]
#         results = [future.result() for future in futures]

#     results_flat = list(itertools.chain.from_iterable(results))

#     return results_flat


async def get_tickers_data() -> List[ScrapeResult]:
    all_symbols = get_all_symbols()
    # basic_contract_info = parallelized_scrape_basic_contract_info_req(all_symbols)
    index_all = get_index_all_ws()
    ticker_overview = get_ticker_everview_ws()

    # reconcile
    to_return: List[ScrapeResult] = [
        {
            "symbol": symbol,
            # "basic_contract_info": [
            #     data
            #     for data in basic_contract_info
            #     if data["data"]["symbol_name"] == symbol
            # ][0],
            "index_all": [
                data for data in index_all["instruments"] if data["symbol"] == symbol
            ][0],
            "ticker_overview": [
                data for data in ticker_overview["data"] if data["symbol"] == symbol
            ][0],
        }
        for symbol in all_symbols
    ]

    return to_return

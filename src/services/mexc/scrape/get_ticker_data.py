import httpx
from typing_extensions import List

from src.services.mexc.types_ import (
    ContractDetailResponse,
    MexcScrapedTick,
    Ticker,
    TickersResponse,
)


def get_tickers_data() -> List[MexcScrapedTick]:
    tickers_price_data_json: TickersResponse = httpx.get(
        "https://futures.mexc.com/api/v1/contract/ticker"
    ).json()
    price_data = tickers_price_data_json["data"]

    leverage_data_json: ContractDetailResponse = httpx.get(
        "https://futures.mexc.com/api/v1/contract/detailV2"
    ).json()
    leverage_data = leverage_data_json["data"]

    data_to_return: List[MexcScrapedTick] = []
    # match leverage and price datas by symbols
    for price_data_for_symbol in price_data:
        try:
            ld_of_interest = [
                ld
                for ld in leverage_data
                if ld["symbol"] == price_data_for_symbol["symbol"]
            ][0]
        except:
            print(f"WARNING symbol: {price_data_for_symbol['symbol']}")
            continue
        data_to_return.append(
            {"ticker_data": price_data_for_symbol, "contract_data": ld_of_interest}
        )

    return data_to_return


def get_ticker_of_interest(tickers: List[MexcScrapedTick], symbol: str):
    for ticker in tickers:
        if ticker["ticker_data"]["symbol"] == symbol:
            return ticker

    raise ValueError(f"Ticker with symbol '{symbol}' was not found")


def get_ticker_data(symbol: str) -> MexcScrapedTick:
    tickers = get_tickers_data()
    ticker = get_ticker_of_interest(tickers, symbol)
    return ticker

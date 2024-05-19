import httpx
from typing_extensions import List

from src.services.mexc.types_ import Ticker, TickersResponse


def get_tickers_data() -> List[Ticker]:
    tickers_data: TickersResponse = httpx.get(
        "https://futures.mexc.com/api/v1/contract/ticker"
    ).json()
    tickers = tickers_data["data"]
    return tickers


def get_ticker_of_interest(tickers: List[Ticker], symbol: str):
    for ticker in tickers:
        if ticker["symbol"] == symbol:
            return ticker

    raise ValueError(f"Ticker with symbol '{symbol}' was not found")


def get_ticker_data(symbol: str) -> Ticker:
    tickers = get_tickers_data()
    ticker = get_ticker_of_interest(tickers, symbol)
    return ticker

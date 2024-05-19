from datetime import datetime, timezone

import httpx
from typing_extensions import List

from src.services.mexc.types_ import Ticker, TickerShort, TickersResponse


def get_tickers_short_data() -> List[TickerShort]:
    tickers_data: TickersResponse = httpx.get(
        "https://futures.mexc.com/api/v1/contract/ticker"
    ).json()
    tickers = tickers_data["data"]
    tickers_short = [
        TickerShort(
            symbol=ticker["symbol"],
            lastPrice_indeksnaCina=ticker["lastPrice"],
            indexPrice=ticker["indexPrice"],
            fairPrice_cinaMarkuvannya=ticker["fairPrice"],
            fundingRate_stavkaFinansuvannya=ticker["fundingRate"],
            timestamp=ticker["timestamp"],
            timestamp_iso=datetime.fromtimestamp(
                ticker["timestamp"] / 1000, timezone.utc
            ).isoformat(),
        )
        for ticker in tickers
    ]
    return tickers_short


def get_ticker_of_interest(tickers: List[TickerShort], symbol: str):
    for ticker in tickers:
        if ticker["symbol"] == symbol:
            return ticker

    raise ValueError(f"Ticker with symbol '{symbol}' was not found")


def get_ticker_short_data(symbol: str) -> TickerShort:
    tickers = get_tickers_short_data()
    ticker = get_ticker_of_interest(tickers, symbol)
    return ticker

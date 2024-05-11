from typing_extensions import List

from src.db.repositories.mexc.TickerTimeseries import (
    add_ticker_update,
    get_ticker_timeseries,
)
from src.services.scrapers.mexc.checks_notifications import check_run_notifications
from src.services.scrapers.mexc.get_ticker_data import get_tickers_data
from src.services.scrapers.mexc.types_ import TickerAnalyticsDataPoint


def periodic_task(execution_timestamp: str):
    "scrape, create object, persist in db"
    "get from db, analyze, notify"
    scrape_update_db(execution_timestamp)
    analysis_notif_send()


def scrape_update_db(execution_timestamp: str):
    "scrape, create object, persist in db"
    latest_tickers = get_tickers_data()

    latest_tickers_my_format: List[TickerAnalyticsDataPoint] = [
        {
            "symbol": ticker["symbol"],
            "timestamp": execution_timestamp,
            "last_price": ticker["lastPrice"],
            "fair_price": ticker["fairPrice"],
            "last_div_fair": ticker["lastPrice"] / ticker["fairPrice"],
            "delta_div_avg": (ticker["lastPrice"] - ticker["fairPrice"])
            / ((ticker["lastPrice"] + ticker["fairPrice"]) / 2),
        }
        for ticker in latest_tickers
    ]

    for data_point in latest_tickers_my_format:
        add_ticker_update(data_point)


def analysis_notif_send():
    "get from db, analyze, notify"
    ticker_timeseries = get_ticker_timeseries("BTC_USDT", steps=10)
    check_run_notifications(ticker_timeseries)

from typing_extensions import List

from src.db.repositories.mexc.TickerTimeseries import (
    add_ticker_update,
    add_tickers_updates,
    get_ticker_timeseries,
)
from src.services.mexc.notifications.historic.main import (
    main as historic_notifications_main,
)
from src.services.mexc.notifications.insta.main import main as insta_notifications_main
from src.services.mexc.scrape.get_ticker_data import get_tickers_data
from src.services.mexc.types_ import TickerAnalyticsDataPoint
from src.utils.utils import timeit_context


def periodic_task(execution_timestamp: str):
    "scrape, create object, persist in db"
    "get from db, analyze, notify"
    with timeit_context("mexc full execution"):
        with timeit_context("mexc scraping"):
            latest_tickers_data_points = scrape_update_db(execution_timestamp)
            print(f"mexc n_symbols: {len(latest_tickers_data_points)}")
        with timeit_context("mexc notifs"):
            analysis_notif_send(latest_tickers_data_points)


def scrape_update_db(execution_timestamp: str) -> List[TickerAnalyticsDataPoint]:
    "scrape, create object, persist in db. return current data points"
    latest_tickers = get_tickers_data()

    latest_tickers_my_format: List[TickerAnalyticsDataPoint] = [
        {
            "symbol": ticker["ticker_data"]["symbol"],
            "timestamp": execution_timestamp,
            "last_price": ticker["ticker_data"]["lastPrice"],
            "fair_price": ticker["ticker_data"]["fairPrice"],
            "index_price": ticker["ticker_data"]["indexPrice"],
            "funding_rate": ticker["ticker_data"]["fundingRate"],
            "leverage_max": ticker["contract_data"]["maxL"],
            #
            "index_fair_delta_div_index": (
                ticker["ticker_data"]["indexPrice"] - ticker["ticker_data"]["fairPrice"]
            )
            / ticker["ticker_data"]["indexPrice"],
            "fair_last_delta_div_fair": (
                ticker["ticker_data"]["fairPrice"] - ticker["ticker_data"]["lastPrice"]
            )
            / ticker["ticker_data"]["fairPrice"],
            #
            "last_fair_delta_div_avg": (
                ticker["ticker_data"]["lastPrice"] - ticker["ticker_data"]["fairPrice"]
            )
            / (
                (
                    ticker["ticker_data"]["lastPrice"]
                    + ticker["ticker_data"]["fairPrice"]
                )
                / 2
            ),
        }
        for ticker in latest_tickers
    ]

    add_tickers_updates(latest_tickers_my_format)

    return latest_tickers_my_format


def analysis_notif_send(latest_tickers_data_points: List[TickerAnalyticsDataPoint]):
    "(not) get from db, analyze, notify"
    # ticker_timeseries = get_ticker_timeseries("BTC_USDT", steps=10)
    for data_point in latest_tickers_data_points:
        symbol = data_point["symbol"]

        insta_notifications_main(data_point, symbol)

        ticker_timeseries = get_ticker_timeseries(symbol, steps=10)
        historic_notifications_main(ticker_timeseries, symbol)

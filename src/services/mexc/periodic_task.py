from typing_extensions import List

from src.db.repositories.mexc.TickerTimeseries import (
    add_ticker_update,
    get_ticker_timeseries,
)
from src.services.mexc.notifications.historic.main import (
    main as historic_notifications_main,
)
from src.services.mexc.notifications.insta.main import main as insta_notifications_main
from src.services.mexc.scrape.get_ticker_data import get_tickers_data
from src.services.mexc.types_ import TickerAnalyticsDataPoint


def periodic_task(execution_timestamp: str):
    "scrape, create object, persist in db"
    "get from db, analyze, notify"
    latest_tickers_data_points = scrape_update_db(execution_timestamp)
    analysis_notif_send(latest_tickers_data_points)


def scrape_update_db(execution_timestamp: str) -> List[TickerAnalyticsDataPoint]:
    "scrape, create object, persist in db. return current data points"
    latest_tickers = get_tickers_data()

    latest_tickers_my_format: List[TickerAnalyticsDataPoint] = [
        {
            "symbol": ticker["symbol"],
            "timestamp": execution_timestamp,
            "last_price": ticker["lastPrice"],
            "fair_price": ticker["fairPrice"],
            "index_price": ticker["indexPrice"],
            "funding_rate": ticker["fundingRate"],
            #
            "index_fair_delta_div_index": (ticker["indexPrice"] - ticker["fairPrice"])
            / ticker["indexPrice"],
            "fair_last_delta_div_fair": (ticker["fairPrice"] - ticker["lastPrice"])
            / ticker["fairPrice"],
            #
            "last_fair_delta_div_avg": (ticker["lastPrice"] - ticker["fairPrice"])
            / ((ticker["lastPrice"] + ticker["fairPrice"]) / 2),
        }
        for ticker in latest_tickers
    ]

    for data_point in latest_tickers_my_format:
        add_ticker_update(data_point)

    return latest_tickers_my_format


def analysis_notif_send(latest_tickers_data_points: List[TickerAnalyticsDataPoint]):
    "(not) get from db, analyze, notify"
    # ticker_timeseries = get_ticker_timeseries("BTC_USDT", steps=10)
    for data_point in latest_tickers_data_points:
        symbol = data_point["symbol"]

        insta_notifications_main(data_point, symbol)

        ticker_timeseries = get_ticker_timeseries(symbol, steps=10)
        historic_notifications_main(ticker_timeseries, symbol)

from typing_extensions import List

from src.db.repositories.lbank.TickerTimeseries import (
    add_tickers_updates,
    get_ticker_timeseries,
)
from src.services.lbank.notifications.historic.main import (
    main as historic_notifications_main,
)
from src.services.lbank.notifications.insta.main import main as insta_notifications_main
from src.services.lbank.scrape.get_ticker_data import get_tickers_data
from src.services.lbank.types_ import TickerAnalyticsDataPoint
from src.utils.utils import timeit_context


async def periodic_task(execution_timestamp: str):
    "scrape, create object, persist in db"
    "get from db, analyze, notify"
    with timeit_context("lbank full execution"):
        with timeit_context("lbank scraping"):
            latest_tickers_data_points = await scrape_update_db(execution_timestamp)
            print(f"lbank n_symbols: {len(latest_tickers_data_points)}")
        with timeit_context("lbank notifs"):
            analysis_notif_send(latest_tickers_data_points)


async def scrape_update_db(execution_timestamp: str) -> List[TickerAnalyticsDataPoint]:
    "scrape, create object, persist in db. return current data points"
    latest_tickers = await get_tickers_data()

    latest_tickers_my_format: List[TickerAnalyticsDataPoint] = []

    for ticker in latest_tickers:
        try:
            last_price = float(ticker["data_from_ws"]["data_point"]["LastPrice"])  # type: ignore
        except:
            last_price = -1
        try:
            mark_price = float(ticker["data_from_ws"]["data_point"]["MarkedPrice"])  # type: ignore
        except:
            mark_price = -1
        try:
            index_price = float(ticker["data_from_ws"]["data_point"]["UnderlyingPrice"])  # type: ignore
        except:
            index_price = -1

        ticker_my_format: TickerAnalyticsDataPoint = {
            "symbol": ticker["symbol"],
            "timestamp": execution_timestamp,
            "last_price": last_price,
            "mark_price": mark_price,
            "index_price": index_price,
            #
            "index_mark_delta_div_index": (index_price - mark_price) / index_price,
            "mark_last_delta_div_mark": (mark_price - last_price) / mark_price,
        }
        latest_tickers_my_format.append(ticker_my_format)

    add_tickers_updates(latest_tickers_my_format)

    return latest_tickers_my_format


def analysis_notif_send(tickers_data_points: List[TickerAnalyticsDataPoint]):
    "(not) get from db, analyze, notify"
    for data_point in tickers_data_points:
        symbol = data_point["symbol"]
        insta_notifications_main(data_point, symbol)

        ticker_timeseries = get_ticker_timeseries(symbol, steps=10)
        historic_notifications_main(ticker_timeseries, symbol)


def analysis_notif_send_wrapper(
    latest_tickers_data_points: List[TickerAnalyticsDataPoint],
):
    "(not) get from db, analyze, notify"
    for data_point in latest_tickers_data_points:
        symbol = data_point["symbol"]
        insta_notifications_main(data_point, symbol)

        ticker_timeseries = get_ticker_timeseries(symbol, steps=10)
        historic_notifications_main(ticker_timeseries, symbol)

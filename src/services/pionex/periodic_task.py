from typing_extensions import List

from src.db.repositories.pionex.TickerTimeseries import (
    add_tickers_updates,
    get_ticker_timeseries,
)
from src.services.pionex.notifications.historic.main import (
    main as historic_notifications_main,
)
from src.services.pionex.notifications.insta.main import (
    main as insta_notifications_main,
)
from src.services.pionex.scrape.get_ticker_data import get_tickers_data
from src.services.pionex.types_ import TickerAnalyticsDataPoint
from src.utils.utils import timeit_context


async def periodic_task(execution_timestamp: str):
    "scrape, create object, persist in db"
    "get from db, analyze, notify"
    with timeit_context("pionex full execution"):
        with timeit_context("pionex scraping"):
            latest_tickers_data_points = await scrape_update_db(execution_timestamp)
            print(f"pionex n_symbols: {len(latest_tickers_data_points)}")
        with timeit_context("pionex notifs"):
            analysis_notif_send(latest_tickers_data_points)


async def scrape_update_db(execution_timestamp: str) -> List[TickerAnalyticsDataPoint]:
    "scrape, create object, persist in db. return current data points"
    latest_tickers = await get_tickers_data()

    latest_tickers_my_format: List[TickerAnalyticsDataPoint] = [
        {
            "symbol": ticker["symbol"],
            "timestamp": execution_timestamp,
            "last_price": ticker["tickers_price_data"]["p"],
            "index_price": ticker["futures_indexes_data"]["ip"],
            "mark_price": ticker["futures_indexes_data"]["mp"],
            "funding_rate": ticker["futures_indexes_data"]["nfr"],
            "index_mark_delta_div_index": (
                ticker["futures_indexes_data"]["ip"]
                - ticker["futures_indexes_data"]["mp"]
            )
            / ticker["futures_indexes_data"]["ip"],
            "mark_last_delta_div_mark": (
                ticker["futures_indexes_data"]["mp"] - ticker["tickers_price_data"]["p"]
            )
            / ticker["futures_indexes_data"]["mp"],
        }
        for ticker in latest_tickers
    ]

    add_tickers_updates(latest_tickers_my_format)

    return latest_tickers_my_format


def analysis_notif_send(latest_tickers_data_points: List[TickerAnalyticsDataPoint]):
    "(not) get from db, analyze, notify"
    for data_point in latest_tickers_data_points:
        symbol = data_point["symbol"]
        insta_notifications_main(data_point, symbol)

        ticker_timeseries = get_ticker_timeseries(symbol, steps=10)
        historic_notifications_main(ticker_timeseries, symbol)

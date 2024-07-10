from concurrent.futures import ThreadPoolExecutor, wait

from typing_extensions import List

from src.db.repositories.toobit.TickerTimeseries import (
    add_tickers_updates,
    get_ticker_timeseries,
)
from src.services.toobit.notifications.historic.main import (
    main as historic_notifications_main,
)
from src.services.toobit.notifications.insta.main import (
    main as insta_notifications_main,
)
from src.services.toobit.scrape.get_ticker_data import get_tickers_data
from src.services.toobit.types_ import TickerAnalyticsDataPoint
from src.utils.utils import split_list, timeit_context


async def periodic_task(execution_timestamp: str):
    "scrape, create object, persist in db"
    "get from db, analyze, notify"
    with timeit_context("toobit full execution"):
        with timeit_context("toobit scraping"):
            latest_tickers_data_points = await scrape_update_db(execution_timestamp)
            print(f"toobit n_symbols: {len(latest_tickers_data_points)}")
        with timeit_context("toobit notifs"):
            analysis_notif_send(latest_tickers_data_points)


async def scrape_update_db(execution_timestamp: str) -> List[TickerAnalyticsDataPoint]:
    "scrape, create object, persist in db. return current data points"
    latest_tickers = await get_tickers_data()

    latest_tickers_my_format: List[TickerAnalyticsDataPoint] = [
        {
            "symbol": dp["symbol"],
            "timestamp": execution_timestamp,
            "last_price": float(dp["slow_broker"]["c"]),
            "index_price": float(dp["index_price"]["data"][0]["index"]),
            "mark_price": float(dp["mark_price"]["data"][0]["price"]),
            "funding_rate": float(dp["funding_rate"]["fundingRate"]),
            "leverage_max": int(
                float(dp["futures"]["baseTokenFutures"]["maxLeverage"])
            ),
            "index_mark_delta_div_index": (
                float(dp["index_price"]["data"][0]["index"])
                - float(dp["mark_price"]["data"][0]["price"])
            )
            / float(dp["index_price"]["data"][0]["index"]),
            "mark_last_delta_div_mark": (
                float(dp["mark_price"]["data"][0]["price"])
                - float(dp["slow_broker"]["c"])
            )
            / float(dp["mark_price"]["data"][0]["price"]),
        }
        for dp in latest_tickers
    ]

    add_tickers_updates(latest_tickers_my_format)

    return latest_tickers_my_format


def analysis_notif_send(latest_tickers_data_points: List[TickerAnalyticsDataPoint]):
    "(not) get from db, analyze, notify"
    parallelization_level = 10
    task_groups = split_list(latest_tickers_data_points, parallelization_level)

    with ThreadPoolExecutor(max_workers=parallelization_level) as executor:
        futures = [
            executor.submit(analysis_notif_send_, task_group)
            for task_group in task_groups
        ]
        wait(futures)


def analysis_notif_send_(latest_tickers_data_points: List[TickerAnalyticsDataPoint]):
    for data_point in latest_tickers_data_points:
        symbol = data_point["symbol"]
        insta_notifications_main(data_point, symbol)

        ticker_timeseries = get_ticker_timeseries(symbol, steps=10)
        historic_notifications_main(ticker_timeseries, symbol)

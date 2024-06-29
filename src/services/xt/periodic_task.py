from concurrent.futures import ThreadPoolExecutor, wait

from typing_extensions import List

from src.db.repositories.xt.TickerTimeseries import (
    add_tickers_updates,
    get_ticker_timeseries,
)
from src.services.xt.notifications.historic.main import (
    main as historic_notifications_main,
)
from src.services.xt.notifications.insta.main import main as insta_notifications_main
from src.services.xt.scrape.get_ticker_data import get_tickers_data
from src.services.xt.types_ import TickerAnalyticsDataPoint
from src.utils.utils import split_list, timeit_context


async def periodic_task(execution_timestamp: str):
    "scrape, create object, persist in db"
    "get from db, analyze, notify"
    with timeit_context("xt full execution"):
        with timeit_context("xt scraping"):
            latest_tickers_data_points = await scrape_update_db(execution_timestamp)
            print(f"xt n_symbols: {len(latest_tickers_data_points)}")
        with timeit_context("xt notifs"):
            analysis_notif_send(latest_tickers_data_points)


async def scrape_update_db(execution_timestamp: str) -> List[TickerAnalyticsDataPoint]:
    "scrape, create object, persist in db. return current data points"
    latest_tickers = await get_tickers_data()

    latest_tickers_my_format: List[TickerAnalyticsDataPoint] = [
        {
            "symbol": ticker["symbol"],
            "timestamp": execution_timestamp,
            "last_price": ticker["last_price"],
            "index_price": ticker["index_price"],
            "mark_price": ticker["mark_price"],
            "funding_rate": ticker["funding_rate"],
            "index_mark_delta_div_index": (ticker["index_price"] - ticker["mark_price"])
            / ticker["index_price"],
            "mark_last_delta_div_mark": (ticker["mark_price"] - ticker["last_price"])
            / ticker["mark_price"],
        }
        for ticker in latest_tickers
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

from concurrent.futures import ThreadPoolExecutor, wait

from typing_extensions import List

from src.db.repositories.phemex.TickerTimeseries import (
    add_tickers_updates,
    get_ticker_timeseries,
)
from src.services.phemex.notifications.historic.main import (
    main as historic_notifications_main,
)
from src.services.phemex.notifications.insta.main import (
    main as insta_notifications_main,
)
from src.services.phemex.scrape.get_ticker_data import get_tickers_data
from src.services.phemex.types_ import TickerAnalyticsDataPoint
from src.utils.utils import split_list, timeit_context


async def periodic_task(execution_timestamp: str):
    "scrape, create object, persist in db"
    "get from db, analyze, notify"
    with timeit_context("phemex full execution"):
        with timeit_context("phemex scraping"):
            latest_tickers_data_points = await scrape_update_db(execution_timestamp)
            print(f"phemex n_symbols: {len(latest_tickers_data_points)}")
        with timeit_context("phemex notifs"):
            analysis_notif_send(latest_tickers_data_points)


async def scrape_update_db(execution_timestamp: str) -> List[TickerAnalyticsDataPoint]:
    "scrape, create object, persist in db. return current data points"
    latest_tickers = await get_tickers_data()

    latest_tickers_my_format: List[TickerAnalyticsDataPoint] = [
        {
            "symbol": ticker["symbol"],
            "timestamp": execution_timestamp,
            "last_price": ticker["market_data"]["lastRp"],
            "index_price": ticker["market_data"]["indexRp"],
            "mark_price": ticker["market_data"]["markRp"],
            "funding_rate": ticker["market_data"]["fundingRateRr"],
            "index_mark_delta_div_index": (
                ticker["market_data"]["indexRp"] - ticker["market_data"]["markRp"]
            )
            / ticker["market_data"]["indexRp"],
            "mark_last_delta_div_mark": (
                ticker["market_data"]["markRp"] - ticker["market_data"]["lastRp"]
            )
            / ticker["market_data"]["markRp"],
        }
        for ticker in latest_tickers
    ]

    add_tickers_updates(latest_tickers_my_format)

    return latest_tickers_my_format


def analysis_notif_send(latest_tickers_data_points: List[TickerAnalyticsDataPoint]):
    "(not) get from db, analyze, notify"
    # -> {"all_symbols": [], "historic_data": {"<symbol>": {"last_n": [{"<row_from_db>":""}]}}}
    # what if symbols didn't have updates for a long time (is inactive) or just registered
    # pull only symbols that are active -> have update id column, and latest update id record
    # when pulling updates - can pull all that have last update id as update id of interest and some limit - here i can also check that last element is not what expected in terms of update id (given that all ten are returned)
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

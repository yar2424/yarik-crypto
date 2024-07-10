from concurrent.futures import ThreadPoolExecutor, wait

from typing_extensions import List

from src.db.repositories.bitrue.TickerTimeseries import (
    add_tickers_updates,
    get_ticker_timeseries,
)
from src.services.bitrue.notifications.historic.main import (
    main as historic_notifications_main,
)
from src.services.bitrue.notifications.insta.main import (
    main as insta_notifications_main,
)
from src.services.bitrue.scrape.get_ticker_data import get_tickers_data
from src.services.bitrue.types_ import TickerAnalyticsDataPoint
from src.utils.utils import split_list, timeit_context


async def periodic_task(execution_timestamp: str):
    "scrape, create object, persist in db"
    "get from db, analyze, notify"
    with timeit_context("bitrue full execution"):
        with timeit_context("bitrue scraping"):
            latest_tickers_data_points = await scrape_update_db(execution_timestamp)
            print(f"bitrue n_symbols: {len(latest_tickers_data_points)}")
        with timeit_context("bitrue notifs"):
            analysis_notif_send(latest_tickers_data_points)


async def scrape_update_db(execution_timestamp: str) -> List[TickerAnalyticsDataPoint]:
    "scrape, create object, persist in db. return current data points"
    latest_tickers = await get_tickers_data()

    latest_tickers_my_format: List[TickerAnalyticsDataPoint] = [
        {
            "symbol": dp["symbol"],
            "timestamp": execution_timestamp,
            "last_price": dp["ws_info"]["close"],
            "index_price": dp["public_market_info"]["data"]["indexPrice"],
            "mark_price": dp["public_market_info"]["data"]["tagPrice"],
            "funding_rate": dp["public_market_info"]["data"]["currentFundRate"],
            "leverage_max": dp["public_info"]["maxLever"],
            "index_mark_delta_div_index": (
                dp["public_market_info"]["data"]["indexPrice"]
                - dp["public_market_info"]["data"]["tagPrice"]
            )
            / dp["public_market_info"]["data"]["indexPrice"],
            "mark_last_delta_div_mark": (
                dp["public_market_info"]["data"]["tagPrice"] - dp["ws_info"]["close"]
            )
            / dp["public_market_info"]["data"]["tagPrice"],
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

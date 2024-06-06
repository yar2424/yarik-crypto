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


async def periodic_task(execution_timestamp: str):
    "scrape, create object, persist in db"
    "get from db, analyze, notify"
    latest_tickers_data_points = scrape_update_db(execution_timestamp)
    analysis_notif_send(await latest_tickers_data_points)


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
    for data_point in latest_tickers_data_points:
        symbol = data_point["symbol"]
        insta_notifications_main(data_point, symbol)

        ticker_timeseries = get_ticker_timeseries(symbol, steps=10)
        historic_notifications_main(ticker_timeseries, symbol)

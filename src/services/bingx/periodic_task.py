from typing_extensions import List

from src.db.repositories.bingx.TickerTimeseries import (
    add_ticker_update,
    add_tickers_updates,
    get_ticker_timeseries,
)
from src.services.bingx.all_symbols import all_symbols
from src.services.bingx.notifications.main import main as notifications_main
from src.services.bingx.scrape.get_ticker_data import get_tickers_data
from src.services.bingx.types_ import TickerAnalyticsDataPoint


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
            "trade_price": float(ticker["tradePrice"]),
            "fair_price": float(ticker["fairPrice"]),
            "index_price": float(ticker["indexPrice"]),
            "funding_rate": float(ticker["fundingRate"]),
            #
            "index_fair_delta_div_index": (
                float(ticker["indexPrice"]) - float(ticker["fairPrice"])
            )
            / float(ticker["indexPrice"]),
            "fair_trade_delta_div_fair": (
                float(ticker["fairPrice"]) - float(ticker["tradePrice"])
            )
            / float(ticker["fairPrice"]),
        }
        for ticker in latest_tickers
    ]

    # for data_point in latest_tickers_my_format:
    #     add_ticker_update(data_point)
    add_tickers_updates(latest_tickers_my_format)

    return latest_tickers_my_format


def analysis_notif_send(latest_tickers_data_points: List[TickerAnalyticsDataPoint]):
    "(not) get from db, analyze, notify"
    # ticker_timeseries = get_ticker_timeseries("BTC_USDT", steps=10)
    for symbol in all_symbols:
        data_point_of_interest = [
            dp for dp in latest_tickers_data_points if dp["symbol"] == symbol
        ]
        if not data_point_of_interest:
            print(f"WARNING: no symbol '{symbol}' was found in scraped data")
        data_point_of_interest = data_point_of_interest[0]

        notifications_main(data_point_of_interest, symbol)

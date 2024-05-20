from sqlalchemy import desc
from typing_extensions import List

from src.db.engine_session import SessionLocal
from src.db.models.bingx.TickerTimeseries import (
    TickerTimeseries as TickerTimeseriesModel,
)
from src.services.bingx.types_ import TickerAnalyticsDataPoint


def get_ticker_timeseries(symbol: str, steps: int) -> List[TickerAnalyticsDataPoint]:
    with SessionLocal() as session:
        rows = (
            session.query(TickerTimeseriesModel)
            .filter(TickerTimeseriesModel.symbol == symbol)
            .order_by(desc(TickerTimeseriesModel.timestamp))
            .limit(steps)
            .all()
        )
        return [
            {
                "symbol": row.symbol,
                "timestamp": row.timestamp,
                "trade_price": row.trade_price,
                "fair_price": row.fair_price,
                "index_price": row.index_price,
                "funding_rate": row.funding_rate,
                #
                "index_fair_delta_div_index": row.index_fair_delta_div_index,
                "fair_trade_delta_div_fair": row.fair_trade_delta_div_fair,
            }
            for row in rows
        ]


def add_ticker_update(ticker_data_point: TickerAnalyticsDataPoint):
    # add row to db
    with SessionLocal() as session:
        row = TickerTimeseriesModel(
            symbol=ticker_data_point["symbol"],
            timestamp=ticker_data_point["timestamp"],
            trade_price=ticker_data_point["trade_price"],
            fair_price=ticker_data_point["fair_price"],
            index_price=ticker_data_point["index_price"],
            funding_rate=ticker_data_point["funding_rate"],
            #
            index_fair_delta_div_index=ticker_data_point["index_fair_delta_div_index"],
            fair_trade_delta_div_fair=ticker_data_point["fair_trade_delta_div_fair"],
        )
        session.add(row)
        session.commit()


def add_tickers_updates(tickers_data_points: List[TickerAnalyticsDataPoint]):
    rows_to_add = [
        TickerTimeseriesModel(
            symbol=ticker_data_point["symbol"],
            timestamp=ticker_data_point["timestamp"],
            trade_price=ticker_data_point["trade_price"],
            fair_price=ticker_data_point["fair_price"],
            index_price=ticker_data_point["index_price"],
            funding_rate=ticker_data_point["funding_rate"],
            #
            index_fair_delta_div_index=ticker_data_point["index_fair_delta_div_index"],
            fair_trade_delta_div_fair=ticker_data_point["fair_trade_delta_div_fair"],
        )
        for ticker_data_point in tickers_data_points
    ]

    # add rows to db
    with SessionLocal() as session:
        session.bulk_save_objects(rows_to_add)
        session.commit()

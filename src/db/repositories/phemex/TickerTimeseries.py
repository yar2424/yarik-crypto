from sqlalchemy import desc
from typing_extensions import List

from src.db.engine_session import SessionLocal
from src.db.models.phemex.TickerTimeseries import (
    TickerTimeseries as TickerTimeseriesModel,
)
from src.services.phemex.types_ import TickerAnalyticsDataPoint


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
                "last_price": row.last_price,
                "mark_price": row.mark_price,
                "index_price": row.index_price,
                "funding_rate": row.funding_rate,
                #
                "index_mark_delta_div_index": row.index_mark_delta_div_index,
                "mark_last_delta_div_mark": row.mark_last_delta_div_mark,
            }
            for row in rows
        ]


def add_tickers_updates(tickers_data_points: List[TickerAnalyticsDataPoint]):
    rows_to_add = [
        TickerTimeseriesModel(
            symbol=ticker_data_point["symbol"],
            timestamp=ticker_data_point["timestamp"],
            last_price=ticker_data_point["last_price"],
            mark_price=ticker_data_point["mark_price"],
            index_price=ticker_data_point["index_price"],
            funding_rate=ticker_data_point["funding_rate"],
            #
            index_mark_delta_div_index=ticker_data_point["index_mark_delta_div_index"],
            mark_last_delta_div_mark=ticker_data_point["mark_last_delta_div_mark"],
        )
        for ticker_data_point in tickers_data_points
    ]

    # add rows to db
    with SessionLocal() as session:
        session.bulk_save_objects(rows_to_add)
        session.commit()

from sqlalchemy import UUID, Column, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .._base import Base


class TickerTimeseries(Base):
    __tablename__ = "ticker_timeseries_bingx"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    symbol: Mapped[str] = mapped_column()
    timestamp: Mapped[str] = mapped_column()
    trade_price: Mapped[float] = mapped_column()
    fair_price: Mapped[float] = mapped_column()
    index_price: Mapped[float] = mapped_column()
    funding_rate: Mapped[float] = mapped_column()

    index_fair_delta_div_index: Mapped[float] = mapped_column()
    fair_trade_delta_div_fair: Mapped[float] = mapped_column()

    __table_args__ = (Index("idx_symbol_timestamp_bingx", "symbol", "timestamp"),)

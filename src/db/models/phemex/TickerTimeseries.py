from sqlalchemy import UUID, Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .._base import Base


class TickerTimeseries(Base):
    __tablename__ = "ticker_timeseries_phemex"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # update_id: Mapped[int] = mapped_column()

    symbol: Mapped[str] = mapped_column()
    timestamp: Mapped[str] = mapped_column()
    last_price: Mapped[float] = mapped_column()
    mark_price: Mapped[float] = mapped_column()
    index_price: Mapped[float] = mapped_column()
    funding_rate: Mapped[float] = mapped_column()

    index_mark_delta_div_index: Mapped[float] = mapped_column()
    mark_last_delta_div_mark: Mapped[float] = mapped_column()

from sqlalchemy import UUID, Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .._base import Base


class TickerTimeseries(Base):
    __tablename__ = "ticker_timeseries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    symbol: Mapped[str] = mapped_column()
    timestamp: Mapped[str] = mapped_column()
    last_price: Mapped[float] = mapped_column()
    fair_price: Mapped[float] = mapped_column()

    last_div_fair: Mapped[float] = mapped_column()
    delta_div_avg: Mapped[float] = mapped_column()

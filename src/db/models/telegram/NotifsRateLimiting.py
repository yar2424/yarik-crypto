from sqlalchemy import UUID, Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .._base import Base


class NotifsRateLimiting(Base):
    __tablename__ = "notifs"

    notif_name: Mapped[str] = mapped_column(primary_key=True)
    last_sent: Mapped[str] = mapped_column()

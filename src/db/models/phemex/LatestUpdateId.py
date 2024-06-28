from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from .._base import Base


class LatestUpdateId(Base):
    __tablename__ = "latest_update_id_phemex"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )  # for table to work

    update_id: Mapped[int] = mapped_column()

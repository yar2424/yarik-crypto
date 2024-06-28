from typing import Optional

from sqlalchemy.orm import Session

from src.db.engine_session import SessionLocal
from src.db.models.phemex.LatestUpdateId import LatestUpdateId as LatestUpdateIdModel


def get_latest_update_id() -> int:
    with SessionLocal() as session:
        row = session.query(LatestUpdateIdModel).first()
        return row.update_id if row else 0


def set_latest_update_id(update_id: int):
    with SessionLocal() as session:
        row = session.query(LatestUpdateIdModel).first()
        if row:
            row.update_id = update_id
        else:
            row = LatestUpdateIdModel(update_id=update_id)
            session.add(row)
        session.commit()

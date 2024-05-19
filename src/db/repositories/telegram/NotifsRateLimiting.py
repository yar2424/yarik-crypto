from datetime import datetime

from sqlalchemy import desc
from typing_extensions import List, Optional

from src.db.engine_session import SessionLocal
from src.db.models.telegram.NotifsRateLimiting import (
    NotifsRateLimiting as NotifsRateLimitingModel,
)
from src.services.mexc.types_ import TickerAnalyticsDataPoint

# update
# get last sent timestamp


def update_last_sent_now(notif_name: str):
    update_last_sent(notif_name, datetime.utcnow())


def update_last_sent(notif_name: str, last_sent: datetime):
    with SessionLocal() as session:
        row = (
            session.query(NotifsRateLimitingModel)
            .filter(NotifsRateLimitingModel.notif_name == notif_name)
            .first()
        )
        if not row:
            row = NotifsRateLimitingModel(notif_name=notif_name)
        row.last_sent = last_sent.isoformat()
        session.add(row)
        session.commit()


def get_last_sent(notif_name: str) -> Optional[datetime]:
    with SessionLocal() as session:
        row = (
            session.query(NotifsRateLimitingModel)
            .filter(NotifsRateLimitingModel.notif_name == notif_name)
            .first()
        )
        if row:
            return datetime.fromisoformat(row.last_sent)
        return datetime.fromtimestamp(1)

from src.db.engine_session import engine
from src.db.models._base import Base  # Import base

# Importing the models is essential for create_all to recognize them
from src.db.models.bingx.TickerTimeseries import TickerTimeseries
from src.db.models.mexc.TickerTimeseries import TickerTimeseries
from src.db.models.telegram.NotifsRateLimiting import NotifsRateLimiting


def create_tables():
    Base.metadata.drop_all(engine)

    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()

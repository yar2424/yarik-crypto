import pytest
from typing_extensions import List

from src.db.repositories.phemex.TickerTimeseries import (
    add_tickers_updates,
    get_ticker_timeseries,
)
from src.services.phemex.notifications.historic.main import (
    main as historic_notifications_main,
)
from src.services.phemex.notifications.insta.main import (
    main as insta_notifications_main,
)
from src.services.phemex.periodic_task import periodic_task
from src.services.phemex.scrape.get_ticker_data import get_tickers_data
from src.services.phemex.types_ import TickerAnalyticsDataPoint
from src.utils.utils import timeit_context


@pytest.mark.asyncio
async def test_periodic_task():
    result = await periodic_task("tstmp")
    print(result)

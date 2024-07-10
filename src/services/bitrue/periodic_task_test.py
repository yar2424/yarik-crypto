from concurrent.futures import ThreadPoolExecutor, wait

import pytest
from typing_extensions import List

from src.db.repositories.bitrue.TickerTimeseries import (
    add_tickers_updates,
    get_ticker_timeseries,
)
from src.services.bitrue.notifications.historic.main import (
    main as historic_notifications_main,
)
from src.services.bitrue.notifications.insta.main import (
    main as insta_notifications_main,
)
from src.services.bitrue.periodic_task import periodic_task
from src.services.bitrue.scrape.get_ticker_data import get_tickers_data
from src.services.bitrue.types_ import TickerAnalyticsDataPoint
from src.utils.utils import split_list, timeit_context


@pytest.mark.debug_test
@pytest.mark.asyncio
async def test_periodic_task():
    await periodic_task("123")
    print()

import asyncio
import sys

sys.path.insert(0, "/Users/philip/Documents/projects/yarik/crypto_price_scraper/")

from src.services.lbank.scrape.get_ticker_data import (
    get_data_with_browser_headers_and_custom_requests,
)

asyncio.run(get_data_with_browser_headers_and_custom_requests())

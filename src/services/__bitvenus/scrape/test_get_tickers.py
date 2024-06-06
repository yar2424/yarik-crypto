import asyncio
import sys

sys.path.insert(0, "/Users/philip/Documents/projects/yarik/crypto_price_scraper/")

from src.services.bitvenus.scrape.get_ticker_data import get_tickers_data

if __name__ == "__main__":
    asyncio.run(get_tickers_data())

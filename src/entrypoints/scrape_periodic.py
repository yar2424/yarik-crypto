import asyncio
import time

import schedule

from src.config import config
from src.services.periodic_tasks.periodic_scrape import periodic_scrape


def main():
    def periodic_task():
        asyncio.run(periodic_scrape())

    schedule.every(config["check_every_seconds"]).minutes.do(periodic_task)

    while True:
        schedule.run_pending()
        time.sleep(0.1)


if __name__ == "__main__":
    main()

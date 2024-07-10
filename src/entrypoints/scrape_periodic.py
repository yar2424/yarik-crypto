import asyncio
import time
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

from src.config import config
from src.services.periodic_tasks.periodic_scrape import (
    periodic_scrape_every_1_min,
    periodic_scrape_every_2_min,
)


def main():
    def periodic_task_1():
        asyncio.run(periodic_scrape_every_1_min())

    def periodic_task_2():
        asyncio.run(periodic_scrape_every_2_min())

    scheduler = BackgroundScheduler()

    now = datetime.now()
    start_time = now.replace(second=0, microsecond=0) + timedelta(minutes=1)
    # start_time = now.replace(second=0, microsecond=0)

    scheduler.add_job(
        periodic_task_1,
        "interval",
        seconds=config["check_every_seconds"],
        start_date=start_time,
        max_instances=3,
    )

    scheduler.add_job(
        periodic_task_2,
        "interval",
        seconds=120,
        start_date=start_time,
        max_instances=3,
    )

    scheduler.start()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == "__main__":
    main()

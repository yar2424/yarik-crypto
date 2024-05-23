import asyncio
import time
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from src.config import config
from src.services.periodic_tasks.periodic_scrape import periodic_scrape


def main():
    def periodic_task():
        asyncio.run(periodic_scrape())

    scheduler = BackgroundScheduler()

    now = datetime.now()
    # start_time = (now.replace(second=0, microsecond=0) + timedelta(minutes=1))
    start_time = now.replace(second=0, microsecond=0)

    scheduler.add_job(
        periodic_task,
        "interval",
        seconds=config["check_every_seconds"],
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

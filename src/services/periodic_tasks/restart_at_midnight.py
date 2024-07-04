import asyncio
import time
from datetime import datetime, timedelta

import boto3
from apscheduler.schedulers.background import BackgroundScheduler

from src.config import config
from src.services.periodic_tasks.periodic_scrape import periodic_scrape


def trigger_ecs_deployment():
    ecs_client = boto3.client("ecs")
    response = ecs_client.update_service(
        cluster=config["ecs_cluster"],
        service=config["ecs_service"],
        forceNewDeployment=True,
    )
    return response


def main():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        trigger_ecs_deployment,
        "cron",
        hour=0,
        minute=0,
        max_instances=3,
    )

    scheduler.start()

    try:
        # Keeps the main thread alive by joining the scheduler's thread
        scheduler._thread.join()  # type: ignore
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == "__main__":
    main()

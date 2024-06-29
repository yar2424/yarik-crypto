import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, wait

from src.services.bingx.periodic_task import periodic_task as periodic_task_bingx
from src.services.lbank.periodic_task import periodic_task as periodic_task_lbank
from src.services.mexc.periodic_task import periodic_task as periodic_task_mexc
from src.services.phemex.periodic_task import periodic_task as periodic_task_phemex
from src.services.pionex.periodic_task import periodic_task as periodic_task_pionex
from src.services.xt.periodic_task import periodic_task as periodic_task_xt
from src.utils.utils import zulu_time_now_str


def async_wrapper(func, *args):
    return asyncio.run(func(*args))


async def periodic_scrape():
    current_timestamp = zulu_time_now_str()

    with ProcessPoolExecutor(max_workers=100) as executor:
        # with ThreadPoolExecutor(max_workers=6) as executor:
        # Schedule the tasks to run in the pool
        futures = [
            executor.submit(async_wrapper, periodic_task_bingx, current_timestamp),
            executor.submit(periodic_task_mexc, current_timestamp),
            executor.submit(async_wrapper, periodic_task_lbank, current_timestamp),
            executor.submit(async_wrapper, periodic_task_xt, current_timestamp),
            executor.submit(async_wrapper, periodic_task_phemex, current_timestamp),
            executor.submit(async_wrapper, periodic_task_pionex, current_timestamp),
        ]

        # Wait for all tasks to complete
        wait(futures)

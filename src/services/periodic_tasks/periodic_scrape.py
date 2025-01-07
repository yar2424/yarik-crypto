import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, wait

from src.services.bingx.periodic_task import periodic_task as periodic_task_bingx
from src.services.bitrue.periodic_task import periodic_task as periodic_task_bitrue
from src.services.bitvenus.periodic_task import periodic_task as periodic_task_bitvenus
from src.services.blofin.periodic_task import periodic_task as periodic_task_blofin
from src.services.lbank.periodic_task import periodic_task as periodic_task_lbank
from src.services.mexc.periodic_task import periodic_task as periodic_task_mexc
from src.services.phemex.periodic_task import periodic_task as periodic_task_phemex
from src.services.pionex.periodic_task import periodic_task as periodic_task_pionex
from src.services.toobit.periodic_task import periodic_task as periodic_task_toobit
from src.services.websea.periodic_task import periodic_task as periodic_task_websea
from src.services.xt.periodic_task import periodic_task as periodic_task_xt
from src.utils.utils import zulu_time_now_str


def async_wrapper(func, *args):
    return asyncio.run(func(*args))


async def periodic_scrape_every_1_min():
    current_timestamp = zulu_time_now_str()

    with ProcessPoolExecutor(max_workers=100) as executor:
        # with ThreadPoolExecutor(max_workers=6) as executor:
        # Schedule the tasks to run in the pool
        futures = [
            #executor.submit(async_wrapper, periodic_task_bingx, current_timestamp),
            executor.submit(periodic_task_mexc, current_timestamp),
            #executor.submit(async_wrapper, periodic_task_lbank, current_timestamp),
            #executor.submit(async_wrapper, periodic_task_xt, current_timestamp),
            #executor.submit(async_wrapper, periodic_task_phemex, current_timestamp),
            #executor.submit(async_wrapper, periodic_task_pionex, current_timestamp),
            #
            #executor.submit(async_wrapper, periodic_task_websea, current_timestamp),
            #executor.submit(async_wrapper, periodic_task_toobit, current_timestamp),
            #executor.submit(async_wrapper, periodic_task_blofin, current_timestamp),
            #executor.submit(async_wrapper, periodic_task_bitrue, current_timestamp),
        ]

        # Wait for all tasks to complete
        wait(futures)


async def periodic_scrape_every_2_min():
    current_timestamp = zulu_time_now_str()

    with ProcessPoolExecutor(max_workers=100) as executor:
        # with ThreadPoolExecutor(max_workers=6) as executor:
        # Schedule the tasks to run in the pool
        futures = [
            # executor.submit(async_wrapper, periodic_task_bitvenus, current_timestamp),
        ]

        # Wait for all tasks to complete
        wait(futures)

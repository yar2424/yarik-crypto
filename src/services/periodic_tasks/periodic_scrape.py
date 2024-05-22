from src.services.bingx.periodic_task import periodic_task as periodic_task_bingx
from src.services.mexc.periodic_task import periodic_task as periodic_task_mexc
from src.utils.utils import zulu_time_now_str


async def periodic_scrape():
    current_timestamp = zulu_time_now_str()
    await periodic_task_bingx(current_timestamp)
    periodic_task_mexc(current_timestamp)

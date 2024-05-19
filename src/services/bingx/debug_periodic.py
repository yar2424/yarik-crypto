import asyncio
from datetime import datetime

from src.services.bingx.periodic_task import periodic_task

asyncio.run(periodic_task(datetime.utcnow().isoformat()))

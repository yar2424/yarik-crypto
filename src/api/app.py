import subprocess
import threading

from fastapi import FastAPI

from src.api.controllers.bingx import router as bingx_router
from src.api.controllers.bitrue import router as bitrue_router
from src.api.controllers.bitvenus import router as bitvenus_router
from src.api.controllers.blofin import router as blofin_router
from src.api.controllers.lbank import router as lbank_router
from src.api.controllers.mexc import router as mexc_router
from src.api.controllers.phemex import router as phemex_router
from src.api.controllers.pionex import router as pionex_router
from src.api.controllers.telegram import router as telegram_router
from src.api.controllers.toobit import router as toobit_router
from src.api.controllers.websea import router as websea_router
from src.api.controllers.xt import router as xt_router
from src.config import config
from src.services.bingx.periodic_task import periodic_task as periodic_task_bingx
from src.services.mexc.periodic_task import periodic_task as periodic_task_mexc
from src.utils.telegram import get_updates, send_message
from src.utils.utils import zulu_time_now_str

app = FastAPI()

app.include_router(telegram_router)
app.include_router(mexc_router, prefix="/mexc")
app.include_router(bingx_router, prefix="/bingx")
app.include_router(lbank_router, prefix="/lbank")
app.include_router(pionex_router, prefix="/pionex")
app.include_router(xt_router, prefix="/xt")
app.include_router(phemex_router, prefix="/phemex")
app.include_router(bitrue_router, prefix="/bitrue")
app.include_router(bitvenus_router, prefix="/bitvenus")
app.include_router(blofin_router, prefix="/blofin")
app.include_router(toobit_router, prefix="/toobit")
app.include_router(websea_router, prefix="/websea")


# for dev purposes
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

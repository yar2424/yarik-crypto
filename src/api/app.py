import subprocess
import threading

from fastapi import FastAPI

from src.api.controllers.bingx import router as bingx_router
from src.api.controllers.lbank import router as lbank_router
from src.api.controllers.mexc import router as mexc_router
from src.api.controllers.phemex import router as phemex_router
from src.api.controllers.pionex import router as pionex_router
from src.api.controllers.telegram import router as telegram_router
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


# for dev purposes
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

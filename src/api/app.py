import subprocess
import threading

from fastapi import FastAPI
from fastapi_restful.tasks import repeat_every

from src.api.controllers.bingx import router as bingx_router
from src.api.controllers.mexc import router as mexc_router
from src.api.controllers.telegram import router as telegram_router
from src.config import config
from src.services.bingx.periodic_task import periodic_task as periodic_task_bingx
from src.services.mexc.periodic_task import periodic_task as periodic_task_mexc
from src.utils.telegram import get_updates, send_message
from src.utils.utils import zulu_time_now_str

app = FastAPI()

app.include_router(telegram_router)
app.include_router(bingx_router, prefix="/bingx")
app.include_router(mexc_router, prefix="/mexc")


# for dev purposes
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

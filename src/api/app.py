import subprocess
import threading

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

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


# add periodic
@app.on_event("startup")
@repeat_every(seconds=config["check_every_seconds"])
async def run_periodic():
    current_timestamp = zulu_time_now_str()
    await periodic_task_bingx(current_timestamp)
    periodic_task_mexc(current_timestamp)


# reply with your chat_id on /start (telegram)
@app.on_event("startup")
def tg_reply_with_chat_id():
    def tg_reply_with_chat_id():
        last_update_id = 0
        while True:
            updates = get_updates(last_update_id)
            for update in updates:
                if "message" in update:
                    chat_id = update["message"]["chat"]["id"]
                    msg = update["message"]["text"]
                    if msg.startswith("/start"):
                        send_message(chat_id, f"Your chat ID is: {chat_id}")
                    last_update_id = update["update_id"]

    thread = threading.Thread(target=tg_reply_with_chat_id, daemon=True)
    thread.start()


# for dev purposes
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

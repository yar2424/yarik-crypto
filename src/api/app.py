import threading

from dotenv import load_dotenv

load_dotenv("/Users/philip/Documents/projects/yarik/crypto_price_scraper/.env")
import subprocess

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from src.api.controllers import router as api_router
from src.services.scrapers.mexc.periodic_task import periodic_task
from src.utils.telegram import get_updates, send_message
from src.utils.utils import zulu_time_now_str

app = FastAPI()

app.include_router(api_router)


# add periodic
@app.on_event("startup")
@repeat_every(seconds=15)
def run_periodic():
    current_timestamp = zulu_time_now_str()
    periodic_task(current_timestamp)


# reply with your chat_id on /start (telegram)
@app.on_event("startup")
def tg_reply_with_chat_id():
    def tg_reply_with_chat_id():
        last_update_id = 0
        while True:
            updates = get_updates(last_update_id)
            print(updates)
            print(last_update_id)
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

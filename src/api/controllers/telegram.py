import httpx
from fastapi import APIRouter

from src.config import config
from src.utils.telegram import send_message_broadcast

router = APIRouter()


@router.get("/send_test_broadcast_notif", tags=["telegram"])
async def send_test_broadcast_notif():
    message = """
BTC is going crazy!

https://futures.mexc.com/ru-RU/exchange/BTC_USDT

<link to table with last n steps>
"""
    send_message_broadcast(message)


@router.get("/send_test_notif", tags=["telegram"])
async def send_test_notif(chat_id: int):
    message = """
BTC is going crazy!

https://futures.mexc.com/ru-RU/exchange/BTC_USDT

<link to table with last n steps>
"""
    payload = {
        "chat_id": chat_id,
        "text": message,
    }
    httpx.post(f"{config['telegram_bot_api_base_url']}/sendMessage", json=payload)

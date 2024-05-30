from datetime import datetime

import httpx
from typing_extensions import List, TypedDict

from src.config import config


def send_message_broadcast_chats(text: str, chats: List[str]):
    for chat in chats:
        send_message_broadcast(text, chat)


def send_message_broadcast(text: str, chat: str = "all"):
    for chat_id in config["telegram_chat_ids"]:
        send_message(chat_id, text, chat)


def _debug_inject(text: str):
    now = datetime.utcnow()
    sent_at = now.isoformat()
    return f"{text} /nSent at: {sent_at}"


def send_message(chat_id: int, text: str, chat: str):
    """Send a message to the specified chat ID and chat via the Telegram bot."""
    chat_of_interest = [chat_ for chat_ in config["chats"] if chat_["name"] == chat][0]

    text = _debug_inject(text)

    url = chat_of_interest["base_url"] + "/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = httpx.post(url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send message: {response.status_code}")
        print(response.text)
        print(url)
        print(payload)


def get_updates(last_update_id: int, chat: str) -> List["Update"]:
    """Retrieve messages from Telegram server."""
    chat_of_interest = [chat_ for chat_ in config["chats"] if chat_["name"] == chat][0]

    url = chat_of_interest["base_url"] + "/getUpdates"
    params = {"timeout": 100, "offset": last_update_id + 1}
    response = httpx.get(url, params=params, timeout=100 + 10)
    if response.status_code == 200:
        return response.json()["result"]
    print(response)
    return []


def escape_markdown_v2(text):
    escape_chars = (
        "-|.!"  # non exhaustive list of characters to be escaped in Telegram MarkdownV2
    )
    return "".join("\\" + char if char in escape_chars else char for char in text)


##
# Schemas
##


class Update(TypedDict):
    update_id: int
    message: "Message"


class Message(TypedDict):
    message_id: int
    chat: "Chat"
    date: int
    text: str


class Chat(TypedDict):
    id: int
    # username: str
    # first_name: str
    # last_name: str

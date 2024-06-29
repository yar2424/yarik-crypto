import threading

from src.config import config
from src.utils.telegram import get_updates, send_message


def main():
    # threads = []
    # for chat in config["chats"]:
    #     thread = threading.Thread(target=polling_id_reply, args=(chat["name"],))
    #     thread.start()
    #     threads.append(thread)
    # thread.join()

    chat = config["chats"][0]
    polling_id_reply(chat["name"])


def polling_id_reply(chat: str):
    last_update_id = 0
    while True:
        print(f"polling tg chat: '{chat}'")
        try:
            updates = get_updates(last_update_id, chat)
        except:
            continue
        # print()
        for update in updates:
            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                msg = update["message"]["text"]
                if msg.startswith("/start"):
                    send_message(chat_id, f"Your chat ID is: {chat_id}", chat)
                last_update_id = update["update_id"]

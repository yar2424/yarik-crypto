from src.utils.telegram import get_updates, send_message


def periodic_tg():
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

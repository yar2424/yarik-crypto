import os

from src.utils.telegram import send_message_broadcast


def main():
    msg = f"Just restarted, my new ip: {os.getenv('ECS_PUBLIC_IP')}"
    send_message_broadcast(text=msg, chat="prior")


if __name__ == "__main__":
    main()

from datetime import datetime


def zulu_time_now_str():
    return datetime.utcnow().isoformat()

import math

from typing_extensions import List, Optional

from src.services.mexc.notifications.notifications.NotifParams import NotifParams

subnotifs: List[NotifParams] = [
    {"name": "10", "threshold": 0.1},
    {"name": "5", "threshold": 0.05},
    {"name": "2", "threshold": 0.02},
]  # in precedence order (only one (the first met) will be fired)


def notif_name_template(subnotif_name: str):
    return f"index_fair-{subnotif_name}"


def should_fire(notif_params: NotifParams, value: float) -> bool:
    if abs(value) > notif_params["threshold"]:
        return True
    return False


def get_notif_to_fire(value: float) -> Optional[str]:
    # chose which subnotif to fire if any
    for subnotif in subnotifs:
        if should_fire(subnotif, value):
            return notif_name_template(subnotif["name"])

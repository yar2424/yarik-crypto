import math

from typing_extensions import List, Optional

from src.services.blofin.notifications.insta.notifications.NotifParams import (
    SubNotifParams,
)

subnotifs: List[SubNotifParams] = [
    {"name": "8", "threshold": 0.08},
    {"name": "4", "threshold": 0.04},
    {"name": "2", "threshold": 0.02},
    # {"name": "1", "threshold": 0.01},
    # {"name": "0_5", "threshold": 0.005},
    # {"name": "0_05", "threshold": 0.0005},
]  # in precedence order (only one (the first met) will be fired)


def notif_name_template(subnotif_name: str):
    return f"mark_last-{subnotif_name}"


def should_fire(notif_params: SubNotifParams, value: float) -> bool:
    if abs(value) > notif_params["threshold"] and abs(value) < 0.9:
        return True
    return False


def get_notif_to_fire(value: float) -> Optional[str]:
    # chose which subnotif to fire if any
    for subnotif in subnotifs:
        if should_fire(subnotif, value):
            return notif_name_template(subnotif["name"])

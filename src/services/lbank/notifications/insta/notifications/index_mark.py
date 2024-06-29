import math

from typing_extensions import List, Optional

from src.services.lbank.notifications.insta.notifications.NotifParams import (
    SubNotifParams,
)

subnotifs: List[SubNotifParams] = [
    {"name": "8", "threshold": 0.08},
    {"name": "4", "threshold": 0.04},
    # {"name": "2_5", "threshold": 0.025},
]  # in precedence order (only one (the first met) will be fired)


def notif_name_template(subnotif_name: str):
    return f"index_mark-{subnotif_name}"


def should_fire(notif_params: SubNotifParams, value: float) -> bool:
    if abs(value) > notif_params["threshold"]:
        return True
    return False


def get_notif_to_fire(value: float) -> Optional[str]:
    # chose which subnotif to fire if any
    for subnotif in subnotifs:
        if should_fire(subnotif, value):
            return notif_name_template(subnotif["name"])

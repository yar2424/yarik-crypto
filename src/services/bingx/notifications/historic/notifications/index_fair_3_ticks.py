import math

from typing_extensions import List, Optional

from services.bingx.notifications.historic.types_ import (
    NotifTriggerParams,
    NotifWithPriority,
)
from src.services.bingx.types_ import TickerAnalyticsDataPoint

notif_name_to_priority = {
    "index_fair-0_05-3_ticks": 1,
    "index_fair-0_5-3_ticks": 1,
    "index_fair-1_3-3_ticks": 1,
    "index_fair-5-3_ticks": 2,
    "index_fair-10-3_ticks": 2,
}


subnotifs: List[NotifTriggerParams] = [
    {"notif_name": "10-3_ticks", "threshold": 0.1},
    {"notif_name": "5-3_ticks", "threshold": 0.05},
    {"notif_name": "1_3-3_ticks", "threshold": 0.013},
    # {"notif_name": "0_5-3_ticks", "threshold": 0.005},
    # {"notif_name": "0_05-3_ticks", "threshold": 0.0005},
]  # in precedence order (only one (the first met) will be fired)


def notif_name_template(subnotif_name: str):
    return f"index_fair-{subnotif_name}"


def should_fire(
    notif_params: NotifTriggerParams, data_points: List[TickerAnalyticsDataPoint]
) -> bool:
    return all(
        [
            data_point["index_fair_delta_div_index"] > notif_params["threshold"]
            for data_point in data_points
        ]
    )


def get_notif_to_fire(
    data_points: List[TickerAnalyticsDataPoint],
) -> Optional[NotifWithPriority]:
    data_points_to_analyze = data_points[-3:]
    # chose which subnotif to fire if any
    for subnotif in subnotifs:
        if should_fire(subnotif, data_points_to_analyze):
            notif_to_fire_name = notif_name_template(subnotif["notif_name"])
            notif_to_fire: NotifWithPriority = {
                "name": notif_to_fire_name,
                "priority": notif_name_to_priority[notif_to_fire_name],
                "last_value": data_points_to_analyze[-1]["index_fair_delta_div_index"],
            }
            return notif_to_fire

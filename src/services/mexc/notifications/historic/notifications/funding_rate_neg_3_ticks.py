import math

from typing_extensions import List, Optional

from src.services.mexc.notifications.historic.types_ import (
    NotifTriggerParams,
    NotifWithPriority,
)
from src.services.mexc.types_ import TickerAnalyticsDataPoint


def get_notif_to_fire(
    data_points: List[TickerAnalyticsDataPoint],
) -> Optional[NotifWithPriority]:
    data_points_to_analyze = data_points[-3:]
    # chose which subnotif to fire if any

    should_fire = all(
        [data_point["funding_rate"] < 0 for data_point in data_points_to_analyze]
    )

    if should_fire:
        notif_to_fire_name = "funding_rate_neg"
        notif_to_fire: NotifWithPriority = {
            "name": notif_to_fire_name,
            "priority": 0,
            "last_value": data_points_to_analyze[-1]["funding_rate"],
        }
        return notif_to_fire

from typing_extensions import List, Optional


def get_notif_to_fire(value: float) -> Optional[str]:
    if value < -0.01:
        return "funding_rate_neg_1"

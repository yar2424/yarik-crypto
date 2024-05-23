from typing_extensions import Callable, TypedDict


class NotifWithPriority(TypedDict):
    name: str
    priority: int
    last_value: float


class NotifTriggerParams(TypedDict):
    notif_name: str
    threshold: float

from typing_extensions import Callable, List, TypedDict


class NotifWithPriority(TypedDict):
    name: str
    priority: int
    last_value: float
    chats: List[str]


class NotifTriggerParams(TypedDict):
    notif_name: str
    threshold: float

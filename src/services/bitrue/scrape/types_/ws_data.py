from typing_extensions import Dict, List, TypedDict


class WSEventData(TypedDict):
    amount: str
    close: str
    data: List
    high: str
    low: str
    open: str
    rose: str
    vol: str


class WSScrapeResult(TypedDict):
    symbol: str
    symbol_id: int
    close: float


class WSMessage(TypedDict):
    event_rep: str
    channel: str
    data: Dict[str, WSEventData]

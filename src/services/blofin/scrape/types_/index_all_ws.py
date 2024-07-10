from typing_extensions import List, TypedDict


class IndexAllInstrument(TypedDict):
    channel: str
    symbol: str
    index_price: str
    mark_price: str
    funding_rate: str
    next_funding_time: int
    ts: int


class IndexAllMessage(TypedDict):
    channel: str
    instruments: List[IndexAllInstrument]

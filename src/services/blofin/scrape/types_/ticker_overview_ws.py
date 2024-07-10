from typing_extensions import List, TypedDict


class TickerData(TypedDict):
    channel: str
    symbol: str
    open: str
    close: str
    high: str
    low: str
    quantity: str
    contract_quantity: str
    amount: str
    ts: int
    ask_price: str
    ask_quantity: str
    bid_price: str
    bid_quantity: str
    last: str
    last_quantity: str


class TickerOverviewMessage(TypedDict):
    channel: str
    data: List[TickerData]

from typing_extensions import List, TypedDict


class ParamsDict(TypedDict):
    limit: str
    realtimeInterval: str
    binary: str
    reduceSerial: str


class DataDict(TypedDict):
    exchangeId: int
    symbolId: str
    price: str
    time: int


class MarkPriceMessage(TypedDict):
    symbol: str  # BTC-SWAP-USDT
    topic: str
    params: ParamsDict
    data: List[DataDict]
    f: bool
    sendTime: int
    shared: bool
    id: str

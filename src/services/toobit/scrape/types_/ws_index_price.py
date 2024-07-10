from typing_extensions import List, TypedDict


class ParamsDict(TypedDict):
    limit: str
    realtimeInterval: str
    binary: str
    reduceSerial: str


class DataDict(TypedDict):
    symbol: str
    index: str
    edp: str
    formula: str
    time: int


class IndexPriceMessage(TypedDict):
    symbol: str  # BTCUSDT -> BTC-SWAP-USDT
    symbolName: str
    topic: str
    params: ParamsDict
    data: List[DataDict]
    f: bool
    sendTime: int
    shared: bool
    id: str

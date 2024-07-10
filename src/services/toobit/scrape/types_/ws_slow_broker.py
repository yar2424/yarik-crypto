from typing_extensions import List, TypedDict


class SlowBrokerDataEntry(TypedDict):
    t: int
    s: str  # BTC-SWAP-USDT
    sn: str
    c: str
    h: str
    l: str
    o: str
    v: str
    qv: str
    m: str
    e: int
    c24h: str
    h24h: str
    l24h: str
    o24h: str
    v24h: str
    qv24h: str
    m24h: str


class Params(TypedDict):
    realtimeInterval: str
    reduceSerial: str


class SlowBrokerMessage(TypedDict):
    topic: str
    params: Params
    data: List[SlowBrokerDataEntry]
    f: bool
    sendTime: int
    shared: bool
    id: str

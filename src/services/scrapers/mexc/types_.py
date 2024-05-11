from typing_extensions import List, TypedDict


class RiseFallRates(TypedDict):
    zone: str
    r: float
    v: float
    r7: float
    r30: float
    r90: float
    r180: float
    r365: float


class Ticker(TypedDict):  # ContractData
    contractId: int
    symbol: str
    lastPrice: float
    bid1: float
    ask1: float
    volume24: int
    amount24: float
    holdVol: int
    lower24Price: float
    high24Price: float
    riseFallRate: float
    riseFallValue: float
    indexPrice: float
    fairPrice: float
    fundingRate: float
    maxBidPrice: float
    minAskPrice: float
    timestamp: int
    riseFallRates: RiseFallRates
    riseFallRatesOfTimezone: List[float]


class TickerShort(TypedDict):  # ContractData
    symbol: str
    lastPrice_indeksnaCina: float
    indexPrice: float
    fairPrice_cinaMarkuvannya: float
    fundingRate_stavkaFinansuvannya: float
    timestamp: int
    timestamp_iso: str


class TickersResponse(TypedDict):
    success: bool
    code: int
    data: List[Ticker]


class TickerAnalyticsDataPoint(TypedDict):
    symbol: str
    timestamp: str
    last_price: float
    fair_price: float
    last_div_fair: float
    delta_div_avg: float  # (lastPrice - fairPrice) / ((lastPrice + fairPrice) / 2)


class MarketData(TypedDict):
    symbol: str
    lastPrice: float
    riseFallRate: float
    fairPrice: float
    indexPrice: float
    volume24: int
    amount24: float
    maxBidPrice: float
    minAskPrice: float
    lower24Price: float
    high24Price: float
    timestamp: int


class ResponseData(TypedDict):
    data: List[MarketData]

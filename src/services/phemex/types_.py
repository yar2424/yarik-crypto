from typing_extensions import List, TypedDict, Union


class MarketData(TypedDict):
    symbol: str
    openRp: float
    highRp: float
    lowRp: float
    lastRp: float
    volumeRq: float
    turnoverRv: float
    openInterestRv: float
    indexRp: float
    markRp: float
    fundingRateRr: float
    predFundingRateRr: float


class WSMarketDataMsg(TypedDict):
    timestamp: int
    method: str
    type: str
    fields: List[str]
    data: List[List[str]]


class ScrapeResult(TypedDict):
    symbol: str
    market_data: MarketData


class TickerAnalyticsDataPoint(TypedDict):
    symbol: str
    timestamp: str
    last_price: float
    mark_price: float
    index_price: float
    funding_rate: float

    index_mark_delta_div_index: float  # (indexPrice - markPrice) / indexPrice
    mark_last_delta_div_mark: float  # (markPrice - lastPrice) / markPrice

from typing_extensions import Dict, List, TypedDict, Union


class ScrapingResult(TypedDict):
    symbol: str
    last_price: float
    index_price: float
    mark_price: float


class TickerAnalyticsDataPoint(TypedDict):
    symbol: str
    timestamp: str
    trade_price: float
    fair_price: float
    index_price: float
    funding_rate: float

    index_fair_delta_div_index: float  # (indexPrice - fairPrice) / indexPrice
    fair_trade_delta_div_fair: float  # (fairPrice - tradePrice) / fairPrice

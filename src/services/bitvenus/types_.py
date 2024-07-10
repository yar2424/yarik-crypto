from typing_extensions import Dict, List, TypedDict, Union


class ScrapingResult(TypedDict):
    symbol: str
    last_price: float
    index_price: float
    mark_price: float


class TickerAnalyticsDataPoint(TypedDict):
    symbol: str
    timestamp: str
    last_price: float
    mark_price: float
    index_price: float

    index_mark_delta_div_index: float  # (indexPrice - markPrice) / indexPrice
    mark_last_delta_div_mark: float  # (markPrice - lastPrice) / markPrice

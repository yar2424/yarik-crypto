from typing_extensions import TypedDict


class TickerAnalyticsDataPoint(TypedDict):
    symbol: str
    timestamp: str
    last_price: float
    mark_price: float
    index_price: float
    funding_rate: float
    leverage_max: int

    index_mark_delta_div_index: float  # (indexPrice - markPrice) / indexPrice
    mark_last_delta_div_mark: float  # (markPrice - lastPrice) / markPrice

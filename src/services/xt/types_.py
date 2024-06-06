from typing_extensions import List, Optional, TypedDict


class MarkPriceResultEntry(TypedDict):
    s: str  # Symbol (e.g., 'ocean_usdt')
    p: str  # Price (e.g., 0.91603)
    t: int  # Timestamp (e.g., 1717564403147)


class MarkPriceAPIResponse(TypedDict):
    returnCode: int  # Return code (e.g., 0)
    msgInfo: str  # Message information (e.g., 'success')
    error: Optional[str]  # Error message (e.g., None)
    result: List[MarkPriceResultEntry]  # List of result entries


class IndexPriceResultEntry(TypedDict):
    s: str  # Symbol (e.g., 'ocean_usdt')
    p: str  # Price (e.g., 0.91845)
    t: int  # Timestamp (e.g., 1717564902982)


class IndexPriceAPIResponse(TypedDict):
    returnCode: int  # Return code (e.g., 0)
    msgInfo: str  # Message information (e.g., 'success')
    error: Optional[str]  # Error message (e.g., None)
    result: List[IndexPriceResultEntry]  # List of result entries


class TickersDataResultEntry(TypedDict):
    t: int  # Timestamp (e.g., 1717565600528)
    s: str  # Symbol (e.g., 'btc_usdt')
    c: str  # Closing price (e.g., 71022.6)
    h: float  # High price (e.g., 71382.8)
    l: float  # Low price (e.g., 68595.5)
    a: int  # Total amount traded (e.g., 591016658)
    v: int  # Total volume traded (e.g., 4146938761)
    o: float  # Opening price (e.g., 69070.0)
    r: float  # Rate or other related metric (e.g., 0.0282)


class TickersDataAPIResponse(TypedDict):
    returnCode: int  # Return code (e.g., 0)
    msgInfo: str  # Message information (e.g., 'success')
    error: Optional[str]  # Error message (e.g., None)
    result: List[TickersDataResultEntry]  # List of result entries


class FundingRateResult(TypedDict):
    symbol: str  # Symbol (e.g., 'btc_usdt')
    fundingRate: float  # Funding rate (e.g., 0.000104)
    nextCollectionTime: int  # Next collection time (e.g., 1717632000000)
    collectionInternal: int  # Collection interval (e.g., 8)


class FundingRateAPIResponse(TypedDict):
    returnCode: int  # Return code (e.g., 0)
    msgInfo: str  # Message information (e.g., 'success')
    error: Optional[str]  # Error message (e.g., None)
    result: FundingRateResult  # Result entry


class ScrapeResult(TypedDict):
    symbol: str
    mark_price: float
    index_price: float
    last_price: float
    funding_rate: float


class TickerAnalyticsDataPoint(TypedDict):
    symbol: str
    timestamp: str
    last_price: float
    mark_price: float
    index_price: float
    funding_rate: float

    index_mark_delta_div_index: float  # (indexPrice - markPrice) / indexPrice
    mark_last_delta_div_mark: float  # (markPrice - lastPrice) / markPrice

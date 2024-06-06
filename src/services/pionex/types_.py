from typing_extensions import List, Optional, TypedDict


class DataEntry(TypedDict):
    e: str  # Exchange version (e.g., 'pionex.v2')
    b: str  # Base currency (e.g., 'BTC.PERP')
    q: str  # Quote currency (e.g., 'USDT')
    p: str  # Price (e.g., '7088.54')
    h: str  # High price (e.g., '7106.21')
    l: str  # Low price (e.g., '6942.88')
    c: str  # Change percentage (e.g., '0.01297851')
    f: Optional[str]  # Unknown field (e.g., '')
    v: str  # Volume (e.g., '1.836004')
    w: str  # Weighted average price (e.g., '12903.70105135')
    u: str  # Unknown field (e.g., '7088.54')
    tc: Optional[str]  # Unknown field (e.g., '')
    n: str  # Name (e.g., 'yearn.finance')


class DataEntryProperTypes(TypedDict):
    e: str  # Exchange version (e.g., 'pionex.v2')
    b: str  # Base currency (e.g., 'BTC.PERP')
    q: str  # Quote currency (e.g., 'USDT')
    p: float  # Price (e.g., 7088.54)
    h: float  # High price (e.g., 7106.21)
    l: float  # Low price (e.g., 6942.88)
    c: float  # Change percentage (e.g., 0.01297851)
    f: Optional[str]  # Unknown field (e.g., '')
    v: float  # Volume (e.g., 1.836004)
    w: float  # Weighted average price (e.g., 12903.70105135)
    u: float  # Unknown field (e.g., 7088.54)
    tc: Optional[str]  # Unknown field (e.g., '')
    n: str  # Name (e.g., 'yearn.finance')


class TickersPriceData(TypedDict):
    channel: str  # Channel name (e.g., 'tickers.price')
    data: List[DataEntry]  # List of data entries


class IndexDataEntry(TypedDict):
    e: str  # Exchange version (e.g., 'pionex.v2')
    b: str  # Base currency (e.g., 'XAI.PERP')
    q: str  # Quote currency (e.g., 'USDT')
    ip: str  # Index price (e.g., '0.8660884')
    mp: str  # Mark price (e.g., '0.8660884')
    im: str  # Initial margin (e.g., '0.00005')
    nfr: str  # Next funding rate (e.g., '0.00005')
    nft: int  # Next funding timestamp (e.g., 1717560000000)
    t: int  # Timestamp (e.g., 1717559980200)
    s: int  # Status (e.g., 1)


class IndexDataEntryProperTypes(TypedDict):
    e: str  # Exchange version (e.g., 'pionex.v2')
    b: str  # Base currency (e.g., 'XAI.PERP')
    q: str  # Quote currency (e.g., 'USDT')
    ip: float  # Index price (e.g., 0.8660884)
    mp: float  # Mark price (e.g., 0.8660884)
    im: float  # Initial margin (e.g., 0.00005)
    nfr: float  # Next funding rate (e.g., 0.00005)
    nft: int  # Next funding timestamp (e.g., 1717560000000)
    t: int  # Timestamp (e.g., 1717559980200)
    s: int  # Status (e.g., 1)


class FutureIndexesData(TypedDict):
    channel: str  # Channel name (e.g., 'future.indexes')
    data: List[IndexDataEntry]  # List of index data entries


class ScrapeResult(TypedDict):
    symbol: str
    tickers_price_data: DataEntryProperTypes
    futures_indexes_data: IndexDataEntryProperTypes


class TickerAnalyticsDataPoint(TypedDict):
    symbol: str
    timestamp: str
    last_price: float
    mark_price: float
    index_price: float
    funding_rate: float

    index_mark_delta_div_index: float  # (indexPrice - markPrice) / indexPrice
    mark_last_delta_div_mark: float  # (markPrice - lastPrice) / markPrice

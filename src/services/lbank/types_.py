from typing_extensions import Dict, List, Optional, TypedDict, Union

##
# Browser
##


class InstrumentData(TypedDict):
    highestPrice: str
    lowestPrice: str
    instrumentID: str
    change: str
    openPrice: str
    turnover24: str
    highestPrice24: str
    prePositionFeeRate: str
    volume: str
    volume24: str
    change24: str
    lowestPrice24: str
    markedPrice: str
    openPrice24: str
    turnover: str
    lastPrice: str


class MarketDataApiResponse(TypedDict):
    code: int
    data: List[InstrumentData]
    message: str


class AssetBalance(TypedDict):
    balance: str
    frozenMargin: str
    totalCloseProfit: str
    available: str
    crossMargin: str
    frozenFee: str
    marginAble: str


class Data(TypedDict):
    fundingRateTimestamp: int
    isMarketAcount: int
    longMaxVolume: float
    role: int
    openingTime: int
    isCrossMargin: int
    longLeverage: float
    shortLastVolume: float
    longLastVolume: float
    onTime: int
    state: int
    markedPrice: str
    assetBalance: AssetBalance
    longMaxLeverage: int
    unrealProfitCalType: str
    shortMaxVolume: float
    shortLeverage: float
    wsToken: str
    shortMaxLeverage: int
    nextFundingRateTimestamp: int
    forbidTrade: bool
    defaultPositionType: str
    lastPrice: str
    fundingRate: str


class GetDataWithBrowserHeadersAndCustomRequestsReturnTypeElement(TypedDict):
    symbol: str
    data: Optional[Data]


GetDataWithBrowserHeadersAndCustomRequestsReturnType = List[
    GetDataWithBrowserHeadersAndCustomRequestsReturnTypeElement
]


class QryAllApiResponse(TypedDict):
    code: int
    data: Data
    message: str


##
# WS
##


class WSData(TypedDict):
    ExchangeID: str
    InstrumentID: str
    ProductGroup: str
    UpdateTime: str
    UpperLimitPrice: str
    LowerLimitPrice: str
    UnderlyingPrice: str
    MarkedPrice: str
    PositionFeeRate: str
    HighestPrice: str
    LowestPrice: str
    LastPrice: str
    Volume: str
    Turnover: str
    OpenInterest: str
    OpenPrice: str
    InstrumentStatus: str
    PrePositionFeeRate: str
    HighestPrice24: str
    LowestPrice24: str
    Volume24: str
    Turnover24: str
    OpenPrice24: str


class WSResultItem(TypedDict):
    table: str
    data: WSData


class WSMarketDataOverView(TypedDict):
    action: str
    requestNo: int
    errorCode: int
    errorMsg: str
    result: List[WSResultItem]


class WSScrapingResult(TypedDict):
    symbol: str
    data_point: Optional[WSData]


class ScrapeResult(TypedDict):
    symbol: str
    # qry_all_data: Optional[GetDataWithBrowserHeadersAndCustomRequestsReturnTypeElement]
    data_from_ws: Optional[WSScrapingResult]


class TickerAnalyticsDataPoint(TypedDict):
    symbol: str
    timestamp: str
    last_price: float
    mark_price: float
    index_price: float

    index_mark_delta_div_index: float  # (indexPrice - markPrice) / indexPrice
    mark_last_delta_div_mark: float  # (markPrice - lastPrice) / markPrice

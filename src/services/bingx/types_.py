from typing_extensions import Dict, List, TypedDict, Union


class LimitProtect(TypedDict):
    buyMin: str
    buyMax: str
    sellMin: str
    sellMax: str


class Contract(TypedDict):
    contractId: str
    symbol: str
    name: str
    tradePrice: str
    tradeSide: str
    tradeDirection: str
    fairPrice: str
    fairDirection: str
    indexPrice: str
    indexDirection: str
    fundingRate: str
    leftSeconds: str
    size: str
    currency: str
    asset: str
    high: str
    low: str
    open: str
    volume: str
    change: str
    changePercentage: str
    volume2: str
    value: str
    volumeF: float
    valueF: float
    tradingUnit: str
    marketTakeLevel: str
    defaultPrecision: str
    priceDigitNum: int
    qtyDigitNum: int
    tradingPrivilege: int
    status: int
    minQty: str
    minNotional: str
    minStep: str
    weight: int
    triggerProtect: str
    marketProtect: str
    maxOrderNum: int
    limitProtect: LimitProtect
    openTime: int
    openPrice: str
    ensureTrigger: bool
    triggerFeeRate: str
    contractType: str
    priceSource: str
    fundingRateCycle: str
    unrealisedPNL: str
    realisedPNL: str
    unrealisedPNLLong: str
    unrealisedPNLShort: str
    realisedPNLLong: str
    realisedPNLShort: str
    subTradeChannelFlag: int


class Data(TypedDict):
    contracts: List[Contract]


class ApiResponse(TypedDict):
    code: int
    msg: str
    ttl: int
    data: Data


class TickerAnalyticsDataPoint(TypedDict):
    symbol: str
    timestamp: str
    trade_price: float
    fair_price: float
    index_price: float
    funding_rate: float

    index_fair_delta_div_index: float  # (indexPrice - fairPrice) / indexPrice
    fair_trade_delta_div_fair: float  # (fairPrice - tradePrice) / fairPrice

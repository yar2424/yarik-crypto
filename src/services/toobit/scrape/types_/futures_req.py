from typing_extensions import Any, Dict, List, TypedDict


class RiskLimit(TypedDict):
    riskLimitId: str
    riskLimitAmount: str
    maintainMargin: str
    initialMargin: str
    side: str
    maxLeverage: str
    status: int
    white: bool


class BaseTokenFutures(TypedDict):
    tokenId: str
    displayTokenId: str
    quoteTokenId: str
    currency: str
    contractMultiplier: str
    maxLeverage: str
    defaultLeverage: str
    riskLimits: List[RiskLimit]
    marketPriceRange: List[str]
    indexToken: str
    displayIndexToken: str
    marginPrecision: str
    displayUnderlyingId: str


class FuturesSymbol(TypedDict):
    symbolId: str  # BTC-SWAP-USDT
    symbolName: str
    baseTokenId: str
    baseTokenName: str
    quoteTokenId: str
    quoteTokenName: str
    basePrecision: str
    quotePrecision: str
    minPricePrecision: str
    canTrade: bool
    digitMerge: str
    baseTokenFutures: BaseTokenFutures
    secondLevelUnderlyingId: str
    secondLevelUnderlyingName: str
    isReverse: bool
    showStatus: bool
    labelId: int
    label: Dict[str, Any]
    allowPlan: bool
    position: int
    supportPositionType: int
    minTradeQuantity: str
    maxTradeQuantity: str
    minTradeAmount: str
    maxTradeAmount: str
    minBuyPrice: str
    limitMaxSellPrice: str
    limitMinTradeQuantity: str
    limitMaxTradeQuantity: str
    marketMinTradeQuantity: str
    marketMaxTradeQuantity: str
    limitBuyMarkPriceRate: str
    limitSellMarkPriceRate: str
    limitMaxDelegateOrderQuantity: int
    limitMaxConditionOrderQuantity: int
    marketBuyMarkPriceRate: str
    marketSellMarkPriceRate: str
    symbolWeight: int
    icon: str
    closePreviewArea: str
    limitPriceDiffRate: str
    isSupportStrategy: bool
    strategyAdjustCoefficient: str
    strategyAiFloatRatio: str
    virtual: bool


class Data(TypedDict):
    checksum: str
    updated: bool
    futuresSymbol: List[FuturesSymbol]
    futuresCoinToken: List[str]


class FuturesReqResponse(TypedDict):
    code: int
    data: Data

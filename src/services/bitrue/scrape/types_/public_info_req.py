from typing_extensions import Any, List, Mapping, Optional, TypedDict, Union


class CoinResultVo(TypedDict):
    symbolPricePrecision: int
    depth: List[str]
    minOrderVolume: int
    minOrderMoney: float
    maxMarketVolume: int
    maxMarketMoney: float
    maxLimitVolume: int
    maxLimitMoney: float
    priceRange: float
    marginCoinPrecision: int
    fundsInStatus: int
    fundsOutStatus: int


class Contract(TypedDict):
    id: int
    contractName: str
    symbol: str
    contractType: str
    coType: str
    firstTab: str
    contractShowType: str
    deliveryKind: str
    contractSide: int
    multiplier: float
    multiplierCoin: str
    marginCoin: str
    marginRate: float
    capitalStartTime: int
    capitalFrequency: int
    settlementFrequency: int
    brokerId: int
    base: str
    quote: str
    coinResultVo: CoinResultVo
    sort: int
    maxLever: int
    minLever: int
    specialStyle: int


class Data(TypedDict):
    wsUrl: str
    marginCoinList: List[str]
    contractList: List[Contract]


class PublicInfoApiResponse(TypedDict):
    code: str
    msg: str
    args: Optional[Any]
    data: Data
    succ: bool

from typing_extensions import Any, Dict, List, TypedDict


class FundingRatesReqResponseItem(TypedDict):
    tokenId: str  # BTC-SWAP-USDT
    symbolName: str
    settleTime: int
    fundingRate: str
    interest: str
    fundingRateFloor: str
    fundingRateCap: str
    defaultFundingRateFloor: str
    defaultFundingRateCap: str
    period: int
    curServerTime: int

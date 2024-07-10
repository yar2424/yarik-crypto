from typing_extensions import Any, List, Mapping, Optional, TypedDict, Union


class DataDict(TypedDict):
    currentFundRate: float
    indexPrice: float
    remainingSecond: int
    tagPrice: float
    nextFundRate: float


class PublicMarketInfoApiResponse(TypedDict):
    code: str
    msg: str
    args: Optional[None]  # Assuming args can be None
    data: DataDict
    succ: bool


class PublicMarketInfoApiResponseWithId(TypedDict):
    id: int
    code: str
    msg: str
    args: Optional[None]  # Assuming args can be None
    data: DataDict
    succ: bool

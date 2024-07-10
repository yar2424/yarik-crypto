from typing_extensions import List, Mapping, TypedDict, Union


class Headers(TypedDict):
    exchange_token: str
    sec_ch_ua: str
    exchange_language: str
    dfp: str
    ex_sign: str
    sec_ch_ua_mobile: str
    user_agent: str
    content_type: str
    accept: str
    ex_ts: str
    referer: str
    exchange_test_type: str
    exchange_client: str
    sec_ch_ua_platform: str


class QueryParams(TypedDict):
    bitureLanguage: List[str]
    appName: List[str]
    appCodeName: List[str]
    appVersion: List[str]
    userAgent: List[str]
    cookieEnabled: List[str]
    platform: List[str]
    userLanguage: List[str]
    vendor: List[str]
    onLine: List[str]
    product: List[str]
    productSub: List[str]
    mimeTypesLen: List[str]
    pluginsLen: List[str]
    javaEnbled: List[str]
    windowScreenWidth: List[str]
    windowScreenHeight: List[str]
    windowColorDepth: List[str]


class BodyParams(TypedDict):
    contractId: int  # for public_market_info endpoint
    type: str
    uaTime: str
    securityInfo: str


class ReqInfo(TypedDict):
    headers: Headers
    query_params: QueryParams
    body_params: BodyParams
    url: str


class ReqsInfo(TypedDict):
    public_info: ReqInfo
    public_market_info: ReqInfo

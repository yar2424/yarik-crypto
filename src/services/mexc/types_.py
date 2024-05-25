from typing_extensions import List, Optional, TypedDict


class RiseFallRates(TypedDict):
    zone: str
    r: float
    v: float
    r7: float
    r30: float
    r90: float
    r180: float
    r365: float


class Ticker(TypedDict):  # PriceData
    contractId: int
    symbol: str
    lastPrice: float
    bid1: float
    ask1: float
    volume24: int
    amount24: float
    holdVol: int
    lower24Price: float
    high24Price: float
    riseFallRate: float
    riseFallValue: float
    indexPrice: float
    fairPrice: float
    fundingRate: float
    maxBidPrice: float
    minAskPrice: float
    timestamp: int
    riseFallRates: RiseFallRates
    riseFallRatesOfTimezone: List[float]


class TickerShort(TypedDict):  # PriceData
    symbol: str
    lastPrice_indeksnaCina: float
    indexPrice: float
    fairPrice_cinaMarkuvannya: float
    fundingRate_stavkaFinansuvannya: float
    timestamp: int
    timestamp_iso: str


class TickersResponse(TypedDict):
    success: bool
    code: int
    data: List[Ticker]


class ContractDetail(TypedDict):
    symbol: str  # Symbol of the contract pair (e.g., BTC_USDT)
    dn: str  # Display name of the contract in native language
    dne: str  # Display name of the contract in English
    pot: int  # Possibly contract type or category
    bc: str  # Base currency symbol
    qc: str  # Quote currency symbol
    bcn: str  # Base currency name
    qcn: str  # Quote currency name
    ft: int  # Fee type
    sc: str  # Settlement currency
    cs: float  # Contract size or precision
    minL: int  # Minimum leverage
    maxL: int  # Maximum leverage
    ps: int  # Price scale or precision
    vs: int  # Volume scale or precision
    as_: int  # Amount scale or precision
    pu: float  # Price unit or tick size
    vu: int  # Volume unit or tick size
    minV: int  # Minimum volume
    maxV: int  # Maximum volume
    blpr: float  # Base liquidation price rate
    alpr: float  # Additional liquidation price rate
    tfr: float  # Taker fee rate
    mfr: int  # Maker fee rate
    mmr: float  # Maintenance margin rate
    imr: float  # Initial margin rate
    rbv: int  # Risk balance volume
    riv: int  # Risk initial volume
    rlss: int  # Risk level stop spread
    rim: float  # Risk initial margin
    rii: float  # Risk initial interest
    rll: int  # Risk liquidation level
    pcv: float  # Price change value
    io: List[str]  # List of integrated exchanges or platforms
    state: int  # Contract state (e.g., active or inactive)
    in_: bool  # Is the contract active
    ih: bool  # Is the contract in hold
    ihd: bool  # Is the contract in hold detail
    cp: List[str]  # List of categories or tags
    rlt: str  # Ranking type (e.g., by volume)
    mno: List[int]  # Margin no operation (possibly limits or thresholds)
    moml: int  # Margin operation minimum level
    moplr1: float  # Margin operation price level rate 1
    moplr2: float  # Margin operation price level rate 2
    tp: float  # Trading period or time period
    ae: int  # Auto-execute flag or count
    sac: int  # Settlement account
    ad: int  # Additional data or flags
    aa: bool  # Auto-adjust flag
    dsl: List[str]  # Default settlement levels
    lmv: int  # Liquidation margin value
    tsd: int  # Time since default
    bciu: Optional[str]  # Base currency image URL
    id: int  # Contract ID
    vid: str  # Version ID
    bcid: str  # Base currency ID


class ContractDetailResponse(TypedDict):
    success: bool
    code: int
    data: List[ContractDetail]


class MexcScrapedTick(TypedDict):
    ticker_data: Ticker
    contract_data: ContractDetail


class TickerAnalyticsDataPoint(TypedDict):
    symbol: str
    timestamp: str
    last_price: float
    fair_price: float
    index_price: float
    funding_rate: float
    leverage_max: int

    index_fair_delta_div_index: float  # (indexPrice - fairPrice) / indexPrice
    fair_last_delta_div_fair: float  # (fairPrice - lastPrice) / fairPrice

    last_fair_delta_div_avg: (
        float  # (lastPrice - fairPrice) / ((lastPrice + fairPrice) / 2)
    )


class WSMarketData(TypedDict):
    symbol: str
    lastPrice: float
    riseFallRate: float
    fairPrice: float
    indexPrice: float
    volume24: int
    amount24: float
    maxBidPrice: float
    minAskPrice: float
    lower24Price: float
    high24Price: float
    timestamp: int


class WSResponseData(TypedDict):
    data: List[WSMarketData]

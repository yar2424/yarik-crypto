from typing_extensions import List, TypedDict


class BasicContractInfoContractData(TypedDict):
    symbol_name: str
    contract_value: str
    price_precision: str
    tick_size: str
    max_leverage: int
    funding_interval: int
    funding_time: List[str]
    open_interest: str
    insurance_fund: str
    max_limit_order_quantity: int
    max_market_order_quantity: int


class BasicContractInfoApiResponse(TypedDict):
    code: int
    msg: str
    data: BasicContractInfoContractData

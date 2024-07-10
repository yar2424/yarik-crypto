from typing_extensions import TypedDict

from src.services.blofin.scrape.types_.basic_contract_info_req import (
    BasicContractInfoApiResponse,
    BasicContractInfoContractData,
)
from src.services.blofin.scrape.types_.index_all_ws import (
    IndexAllInstrument,
    IndexAllMessage,
)
from src.services.blofin.scrape.types_.ticker_overview_ws import (
    TickerData,
    TickerOverviewMessage,
)


class ScrapeResult(TypedDict):
    symbol: str

    # basic_contract_info: BasicContractInfoApiResponse
    index_all: IndexAllInstrument
    ticker_overview: TickerData

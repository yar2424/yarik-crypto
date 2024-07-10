from typing_extensions import TypedDict

from src.services.websea.scrape.types_.symbol_detail_req import (
    SymbolDetailApiResponse,
    SymbolDetailResult,
)
from src.services.websea.scrape.types_.symbol_list import SymbolListResultItem


class ScrapeResult(TypedDict):
    symbol: str

    symbol_list_data: SymbolListResultItem
    symbol_detail: SymbolDetailResult

from typing_extensions import TypedDict

from src.services.bitrue.scrape.types_.public_info_req import (
    Contract,
    PublicInfoApiResponse,
)
from src.services.bitrue.scrape.types_.public_market_info_req import (
    PublicMarketInfoApiResponseWithId,
)
from src.services.bitrue.scrape.types_.ws_data import WSScrapeResult


class ScrapeResult(TypedDict):
    id: int
    symbol: str
    public_info: Contract
    public_market_info: PublicMarketInfoApiResponseWithId
    ws_info: WSScrapeResult

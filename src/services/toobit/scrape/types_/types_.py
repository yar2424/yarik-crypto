from typing_extensions import TypedDict

from src.services.toobit.scrape.types_.funding_rates_req import (
    FundingRatesReqResponseItem,
)
from src.services.toobit.scrape.types_.futures_req import (
    FuturesReqResponse,
    FuturesSymbol,
)
from src.services.toobit.scrape.types_.ws_index_price import IndexPriceMessage
from src.services.toobit.scrape.types_.ws_mark_price import MarkPriceMessage
from src.services.toobit.scrape.types_.ws_slow_broker import (
    SlowBrokerDataEntry,
    SlowBrokerMessage,
)


class ScrapeResult(TypedDict):
    symbol: str

    slow_broker: SlowBrokerDataEntry
    index_price: IndexPriceMessage
    mark_price: MarkPriceMessage

    futures: FuturesSymbol
    funding_rate: FundingRatesReqResponseItem

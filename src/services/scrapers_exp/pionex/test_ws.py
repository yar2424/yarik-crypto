# %%
import sys

sys.path.insert(0, "/Users/philip/Documents/projects/yarik/crypto_price_scraper")
import json
from collections import Counter
from itertools import chain

from typing_extensions import List
from websocket import create_connection

# %%
ws = create_connection("wss://stream.pionex.com/stream/v2")

# ws.send('{"action":"subscribe","channel":"future.indexes","data":[{"exchange":"pionex.v2","base":"BTC.PERP","quote":"USDT"}]}')
ws.send(
    '{"action":"subscribe","channel":"future.indexes","data":[{"exchange":"pionex.v2"}]}'
)
# ws.send('{"action":"subscribe","channel":"tickers.price","data":[{"exchange":"pionex.v2"},{"exchange":"pionex.v2","base":"BTC.PERP","quote":"USDT"}]}')
# ws.send(
#     '{"action":"subscribe","channel":"tickers.price","data":[{"exchange":"pionex.v2"},{"exchange":"pionex.v2","quote":"USDT"}]}'  # all_symbols, last_price
# )


# %%
for i in range(3):
    msg = json.loads(ws.recv())
    data = msg["data"]
    symbol = "BTC.PERP"
    data_of_interest = [d for d in data if d["b"] == symbol][0]
    print(msg)
    print(data_of_interest)
ws.close()
# %%
ws.close()
msg
# %%
symbols_of_interest_2 = [d["b"] for d in data if d["b"].endswith(".PERP")]

data_of_interest_2 = [d for d in data if d["b"].endswith(".PERP")]
# %%
len(symbols_of_interest_2)
# %%
set(symbols_of_interest_1) - set(symbols_of_interest_2)
# %%
sorted(symbols)
# %%
ws.recv()
data: WSMarketDataMsg = json.loads(ws.recv())
ws.close()


# %%
def market_data_dict_data_point_to_proper_type(
    market_data_dict_data_point: List[str],
) -> MarketData:
    return {
        "symbol": str(market_data_dict_data_point[0]),
        "openRp": float(market_data_dict_data_point[1]),
        "highRp": float(market_data_dict_data_point[2]),
        "lowRp": float(market_data_dict_data_point[3]),
        "lastRp": float(market_data_dict_data_point[4]),
        "volumeRq": float(market_data_dict_data_point[5]),
        "turnoverRv": float(market_data_dict_data_point[6]),
        "openInterestRv": float(market_data_dict_data_point[7]),
        "indexRp": float(market_data_dict_data_point[8]),
        "markRp": float(market_data_dict_data_point[9]),
        "fundingRateRr": float(market_data_dict_data_point[10]),
        "predFundingRateRr": float(market_data_dict_data_point[11]),
    }


# %%
market_data_dict_data_point_to_proper_type(data["data"][0])
# %%

# %%
import sys

sys.path.insert(0, "/Users/philip/Documents/projects/yarik/crypto_price_scraper")
import json
from collections import Counter
from itertools import chain

from typing_extensions import List
from websocket import create_connection

# %%
from src.services.phemex.types_ import MarketData, WSMarketDataMsg

# %%
ws = create_connection("wss://ws10.phemex.com/")

# ws.send('{"method":"perp_market24h_pack.subscribe","params":[],"id":1}')
ws.send('{"method":"perp_market24h_pack_p.subscribe","params":{},"id":2}')
# ws.send('{"method":"spot_market24h_pack.subscribe","params":[],"id":3}')
# ws.send('{"method":"markprice.subscribe","params":[],"id":8}')
# %%

for i in range(3):
    msg = ws.recv()
    print(msg)
    if i == 1:
        with open("out.json", "w+") as f:
            f.write(msg)

ws.close()
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

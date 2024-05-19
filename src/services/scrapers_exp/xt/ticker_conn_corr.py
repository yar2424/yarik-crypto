# %%
import sys

sys.path.insert(0, "/Users/philip/Documents/projects/yarik/crypto_price_scraper")
# %%
import json
from collections import Counter
from itertools import chain

from typing_extensions import List
from websocket import create_connection

from src.services.scrapers.xt.types_ import TickerData

# %%
ws = create_connection("wss://stream.xt.com/public")
# %%
ws.send('{method: "subscribe", params: ["ticker@btc_usdt"]}')
# %%
ws.recv()
# %%
ws.recv()  # {"code":0,"msg":"SUCCESS","method":"unsubscribe"}
ws.recv()  # {"code":0,"msg":"SUCCESS","method":"subscribe"}
received = ws.recv()
received

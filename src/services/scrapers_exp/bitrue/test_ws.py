# %%
import asyncio
import sys
from datetime import datetime, timedelta

import httpx

from src.utils.utils import ungzip_bytes_to_text

sys.path.insert(0, "/Users/philip/Documents/projects/yarik/crypto_price_scraper")
import asyncio

# %%
import json
import urllib.parse
from collections import Counter
from itertools import chain

from playwright.async_api import async_playwright
from typing_extensions import List
from websocket import create_connection

# %%
ws = create_connection("wss://futuresws.bitrue.com/kline-api/ws")
# %%
ws.send('{"event":"req","params":{"channel":"review"}}')
# ws.send(
#     '{"event":"sub","params":{"channel":"market_e_btcusdt_ticker","cb_id":"e_btcusdt"}}'
# )

# %%
text = ungzip_bytes_to_text(ws.recv())
print(text)
# for i in range(3):
# text = ws.recv()
# if i == 1:
#     with open("out.json", "w+") as f:
#         f.write(text)
ws.close()
# %%
data = json.loads(text)
pairs = [d for d in data["data"]]
pairs
# %%

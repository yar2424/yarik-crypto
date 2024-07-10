# %%
import sys

sys.path.insert(0, "/Users/philip/Documents/projects/yarik/crypto_price_scraper")
# %%
import json
from collections import Counter
from itertools import chain

from typing_extensions import List
from websocket import create_connection

from src.services.scrapers_exp.htx.test_ungzip import ungzip_bytes_to_text

# %%
ws = create_connection("wss://www.htx.com/futures/api/swap-ws")
# %%
ws.send('{"sub":"market.overview","zip":1}')
ws.send('{"sub":"market.overview","zip":1}')
# ws.send('{"sub":"market.BTC-USDT.detail","zip":1}')
# %%
for i in range(10):
    text = ungzip_bytes_to_text(ws.recv())
    if i == 1:
        with open("out.json", "w+") as f:
            f.write(text)
    print(text)
ws.close()
# %%
ws.recv()  # {"code":0,"msg":"SUCCESS","method":"unsubscribe"}
ws.recv()  # {"code":0,"msg":"SUCCESS","method":"subscribe"}
received = ws.recv()
received
# %%
data = json.loads(received)["data"]
data = [create_ticker_data(d) for d in data]


# %%
def get_ticker_of_interest(tickers: List[TickerData], symbol: str) -> TickerData:
    for ticker in tickers:
        if ticker["s"] == symbol:
            return ticker
    raise ValueError(f"Ticker with symbol '{symbol}' was not found")


def create_ticker_data(raw_data: dict) -> TickerData:
    return TickerData(
        s=raw_data["s"],
        t=int(raw_data["t"]),
        cv=float(raw_data["cv"]),
        cr=float(raw_data["cr"]),
        o=float(raw_data["o"]),
        c=float(raw_data["c"]),
        h=float(raw_data["h"]),
        l=float(raw_data["l"]),
        q=float(raw_data["q"]),
        v=float(raw_data["v"]),
    )


def fetch_tickers_data():
    ws = create_connection("wss://stream.xt.com/public")

    ws.send('{"method":"unsubscribe","params":["tickers"]}')
    ws.send('{"method":"subscribe","params":["tickers"]}')

    ws.recv()  # {"code":0,"msg":"SUCCESS","method":"unsubscribe"}
    ws.recv()  # {"code":0,"msg":"SUCCESS","method":"subscribe"}
    tickers_json_str = ws.recv()

    data = json.loads(received)["data"]
    tickers = [create_ticker_data(d) for d in data]

    ws.close()

    return tickers


def fetch_ticker_data():
    ws = create_connection("wss://stream.xt.com/public")

    ws.send('{"method":"subscribe","params":["ticker@btc_usdt"]}')

    ws.recv()  # {"code":0,"msg":"SUCCESS","method":"unsubscribe"}
    ws.recv()  # {"code":0,"msg":"SUCCESS","method":"subscribe"}
    tickers_json_str = ws.recv()

    data = json.loads(received)["data"]
    tickers = [create_ticker_data(d) for d in data]

    ws.close()

    return tickers


# %%
tickers = fetch_tickers_data()
get_ticker_of_interest(tickers, "btc_usdt")

# %%
with open("exhaustive_list_of_pairs.json", "w+") as f:
    pairs = sorted([t["s"] for t in tickers])
    obj_to_store = {"pairs": pairs, "num": len(pairs)}
    f.write(json.dumps(obj_to_store))
# %%

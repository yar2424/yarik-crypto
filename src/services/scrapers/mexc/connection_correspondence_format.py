# %%
import json

from types_ import MarketData
from typing_extensions import List
from websocket import create_connection
from collections import Counter
from itertools import chain

# %%
ws = create_connection("wss://futures.mexc.com/edge")
# %%
ws.send('{"method":"sub.tickers","param":{"timezone":"UTC+8"}}')
# %%
received = []
for i in range(10):
    received.append(ws.recv())
received
# %%
ticker_msgs_raw = received[1:]
ticker_msgs: List[List[MarketData]] = [
    json.loads(msg)["data"] for msg in ticker_msgs_raw
]
# %%
all_symbols_occurences_nested = [
    [ticker_data["symbol"] for ticker_data in msg] for msg in ticker_msgs
]
all_symbols_occurences_flat = list(chain.from_iterable(all_symbols_occurences_nested))

# all_fields_occurences_nested = [
#     [list(ticker_data.keys()) for ticker_data in msg] for msg in ticker_msgs
# ]
# all_fields_occurences_flat = list(chain.from_iterable(all_fields_occurences_nested))
# all_fields_occurences_flat = list(chain.from_iterable(all_fields_occurences_flat))

counted = Counter(all_symbols_occurences_flat)
counted
#%%
# Count presence of tickers in messages

"""
for pair in full_list_tickers:
    if pair in current_list_msgs
        add 1 to the counter
"""
"in the end i have some counter that has total number of ticker expected and number observed"

counter = {} # index of list of messages to number present
for idx, msg in enumerate(ticker_msgs):
    present = len(msg)
    counter[idx] = present

for idx in counter:
    print(idx, counter[idx], counter[idx]/356, 356)


# %%

received
# %%
create exhaustive list
#%%
counted.keys()

# %%
with open("exhaustive_list_of_pairs.json", "w+") as f:
    pairs = sorted(list(counted.keys()))
    obj_to_store = {"pairs": pairs, "num": len(pairs)}
    f.write(json.dumps(obj_to_store))
# %%

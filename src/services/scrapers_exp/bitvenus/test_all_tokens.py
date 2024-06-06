# %%
import httpx

# %%
fr_tokens = httpx.get(
    "https://futures.bitvenus.com/api/contract/funding_rates?language=en-us"
).json()
len(fr_tokens)
# %%
all_tokens = httpx.get(
    "https://futures.bitvenus.com/api/v1/basic/all_tokens?language=en-us"
).json()
print(len(all_tokens))
all_swap_tokens = [t for t in all_tokens if "-SWAP-" in t["tokenId"]]
len(all_swap_tokens)
# %%
fr_token_names = [t["tokenId"] for t in fr_tokens]
all_swap_token_names = [t["tokenId"] for t in all_swap_tokens]
# %%
unique_to_fr = set(fr_token_names) - set(all_swap_token_names)
unique_to_all_swap = set(all_swap_token_names) - set(fr_token_names)
# %%
unique_to_fr
# %%
unique_to_all_swap
# %%
url_parts = [t.replace("-SWAP-", "") for t in fr_token_names]
url_parts
# %%

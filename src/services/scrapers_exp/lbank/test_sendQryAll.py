"""
contains leverage
"""

# %%
import time

import httpx

"only one at a time"
url = "https://lbkperp.lbank.com/cfd/agg/v1/sendQryAll"  # requires to be logged in
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "ru",
    "content-encoding": "deflate; g-zip",
    "content-type": "application/json; charset=UTF-8",
    "dnt": "1",
    "ex-browser-name": "Chrome",
    "ex-browser-version": "125.0.0.0",
    "ex-client-source": "WEB",
    "ex-client-type": "WEB",
    "ex-currency": "USD-%24",
    "ex-device-id": "rQPhlVapIHv92yAR978g18l6WBfRDKtZ",
    "ex-language": "ru",
    "ex-language-zh": "%E4%BF%84%E8%AF%AD",
    "ex-os-name": "Mac OS",
    "ex-os-version": "10.15.7",
    "ex-time-zone": "UTC-6",
    "ex-timestamp": str(int(time.time() * 1000)),  # Dynamic timestamp
    "ex-token": "e3e69496b1e84a0caeb85e40d76ef44a",  # maybe will expire
    "ex-uid": "LBA2E28795",
    "origin": "https://www.lbank.com",
    "priority": "u=1, i",
    "referer": "https://www.lbank.com/",
    "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "source": "4",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "versionflage": "true",
}
data = {"productGroup": "SwapU", "instrumentID": "BTCUSDT", "asset": "USDT"}

response = httpx.post(url, headers=headers, json=data)

print("Status Code:", response.status_code)
print("Response Headers:", response.headers)
print("Response JSON:", response.json())

# %%
with open("qry_all_out.json", "w+") as f:
    f.write(response.text)

# %%

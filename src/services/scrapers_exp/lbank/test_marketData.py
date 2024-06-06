# %%
import time

import httpx

# %%
int(time.time())
# %%

url = "https://lbkperp.lbank.com/cfd/instrment/v1/marketData"
current_timestamp = str(int(time.time() * 1000))
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
    "ex-timestamp": current_timestamp,
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
data = {"ProductGroup": "SwapU"}

response = httpx.post(url, headers=headers, json=data)

print(response.status_code)
print(response.json())
# %%

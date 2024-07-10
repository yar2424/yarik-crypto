# %%
import asyncio
import json
from datetime import datetime, timedelta
from urllib.parse import parse_qs, urlparse

import httpx
from playwright.async_api import async_playwright

# %%
# run browser
# goto page
# retrieve url, method, headers, body
# modify body
# make new requests


async def get_reqs_params() -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        should_finish_before = datetime.now() + timedelta(seconds=10)  # for timeout
        should_finish = False  # flip when time to finish (timeout)
        result: dict = {}  # request response data will be stored here

        async def looped_check_update_should_finish():
            "checking until time to update flag and exit"
            while True:
                now = datetime.now()
                if now > should_finish_before:
                    nonlocal should_finish
                    should_finish = True
                    break
                await asyncio.sleep(0.1)

        async def finisher():
            "clean up + return. could also raise error"
            while True:
                if should_finish == True:
                    nonlocal browser, result
                    await browser.close()
                    return result
                await asyncio.sleep(0.1)

        # Event listener to capture and analyze fetch requests
        async def handle_request(request):
            urls_of_interest = {
                "public_info": "https://futures.bitrue.com/fe-co-api/common/public_info",
                "public_market_info": "https://futures.bitrue.com/fe-co-api/common/public_market_info",
            }
            nonlocal result
            if request.url.startswith(urls_of_interest["public_info"]):
                print("in")
                parsed_url = urlparse(request.url)
                query_params = parse_qs(parsed_url.query)
                print(query_params)
                headers = request.headers
                print(headers)
                post_data_str = request.post_data_buffer.decode("utf-8")
                body_params = json.loads(post_data_str)
                print(body_params)

                result.update(
                    {
                        "public_info": {
                            "headers": headers,
                            "query_params": query_params,
                            "body_params": body_params,
                            "url": urls_of_interest["public_info"],
                        }
                    }
                )
                # should return result or error. for now only result or empty dict
            if request.url.startswith(urls_of_interest["public_market_info"]):
                parsed_url = urlparse(request.url)
                query_params = parse_qs(parsed_url.query)
                print(query_params)
                headers = request.headers
                print(headers)

                post_data_str = request.post_data_buffer.decode("utf-8")
                body_params = json.loads(post_data_str)
                print(body_params)

                result.update(
                    {
                        "public_market_info": {
                            "headers": headers,
                            "query_params": query_params,
                            "body_params": body_params,
                            "url": urls_of_interest["public_market_info"],
                        }
                    }
                )

            nonlocal should_finish
            # all required keys in result dict were populated
            all_keys_populated = all(
                [required_key in result for required_key in urls_of_interest]
            )
            if all_keys_populated:
                should_finish = True

        page.on("request", handle_request)

        # Open a webpage
        await page.goto("https://www.bitrue.com/futures/BTC")

        # Start looper
        asyncio.create_task(looped_check_update_should_finish())

        return await finisher()


result = await get_reqs_params()


async def scrape_reqs(reqs_params):
    result = {}
    async with httpx.AsyncClient() as client:
        for key, value in reqs_params.items():
            url = value["url"]
            query_params = {k: v[0] for k, v in value["query_params"].items()}
            headers = value["headers"]
            body_params = value["body_params"]

            response = await client.post(
                url, headers=headers, params=query_params, json=body_params
            )
            result.update({key: response.json()})
    return result


result = await scrape_reqs(result)

result
# %%
# public_info__margin_coin_list = result["public_info"]["data"]["marginCoinList"]
public_info__all_symbols = [
    contract["symbol"] for contract in result["public_info"]["data"]["contractList"]
]
public_info__all_symbols_uni = sorted([
    token.replace('-', "") for token in public_info__all_symbols
]) # 'BTC-USDT' -> 'BTCUSDT'
public_info__all_ids = [
    contract["id"] for contract in result["public_info"]["data"]["contractList"]
]
ws_pairs = [
    "e_1000bonkusdt",
    "e_1000flokiusdt",
    "e_1000luncusdt",
    "e_1000pepeusdt",
    "e_1000ratsusdt",
    "e_1000satsusdt",
    "e_1000shibusdc",
    "e_1000shibusdt",
    "e_1000xecusdt",
    "e_1inchusdt",
    "e_aaveusdt",
    "e_aceusdt",
    "e_achusdt",
    "e_adausd",
    "e_adausdt",
    "e_aevousdt",
    "e_agixusdt",
    "e_agldusdt",
    "e_aiusdt",
    "e_algousd",
    "e_algousdt",
    "e_aliceusdt",
    "e_alphausdt",
    "e_altusdt",
    "e_ambusdt",
    "e_ankrusdt",
    "e_apeusdt",
    "e_api3usdt",
    "e_aptusd",
    "e_aptusdt",
    "e_arbusdt",
    "e_arkmusdt",
    "e_arkusdt",
    "e_arpausdt",
    "e_arusdt",
    "e_astrusdt",
    "e_atausdt",
    "e_atomusdt",
    "e_auctionusdt",
    "e_audiousdt",
    "e_avaxusd",
    "e_avaxusdt",
    "e_axlusdt",
    "e_axsusdt",
    "e_badgerusdt",
    "e_bakeusdt",
    "e_bandusdt",
    "e_batusdt",
    "e_bbusdt",
    "e_bchusdt",
    "e_beamxusdt",
    "e_belusdt",
    "e_bicousdt",
    "e_bigtimeusdt",
    "e_blurusdt",
    "e_blzusdt",
    "e_bnbusd",
    "e_bnbusdt",
    "e_bntusdt",
    "e_bnxusdt",
    "e_bomeusdt",
    "e_bondusdt",
    "e_bsvusdt",
    "e_btcusd",
    "e_btcusdc",
    "e_btcusdt",
    "e_c98usdt",
    "e_cakeusdt",
    "e_celousdt",
    "e_celrusdt",
    "e_cetususdt",
    "e_cfxusdt",
    "e_chrusdt",
    "e_chzusd",
    "e_chzusdt",
    "e_ckbusdt",
    "e_combousdt",
    "e_compusdt",
    "e_coreusdt",
    "e_cotiusdt",
    "e_crvusdt",
    "e_ctcusdt",
    "e_ctsiusdt",
    "e_cyberusdt",
    "e_darusdt",
    "e_dashusdt",
    "e_dentusdt",
    "e_dgbusdt",
    "e_dodoxusdt",
    "e_dogeusd",
    "e_dogeusdc",
    "e_dogeusdt",
    "e_dotusd",
    "e_dotusdt",
    "e_duskusdt",
    "e_dydxusdt",
    "e_dymusdt",
    "e_eduusdt",
    "e_egldusdt",
    "e_enausdt",
    "e_enjusdt",
    "e_ensusdt",
    "e_eosusd",
    "e_eosusdt",
    "e_etcusd",
    "e_etcusdt",
    "e_ethfiusdt",
    "e_ethusd",
    "e_ethusdc",
    "e_ethusdt",
    "e_ethwusdt",
    "e_fetusdt",
    "e_filusd",
    "e_filusdt",
    "e_flmusdt",
    "e_flowusdt",
    "e_frontusdt",
    "e_ftmusd",
    "e_ftmusdt",
    "e_fxsusdt",
    "e_galausdt",
    "e_galusdt",
    "e_gasusdt",
    "e_gftusdt",
    "e_glmrusdt",
    "e_glmusdt",
    "e_gmtusd",
    "e_gmtusdt",
    "e_gmxusdt",
    "e_grtusdt",
    "e_gtcusdt",
    "e_hbarusdt",
    "e_hftusdt",
    "e_hifiusdt",
    "e_highusdt",
    "e_hookusdt",
    "e_hotusdt",
    "e_icpusdt",
    "e_icxusdt",
    "e_idexusdt",
    "e_idusdt",
    "e_ilvusdt",
    "e_imxusdt",
    "e_injusdt",
    "e_iostusdt",
    "e_iotausdt",
    "e_iotxusdt",
    "e_iousdt",
    "e_jasmyusdt",
    "e_joeusdt",
    "e_jtousdt",
    "e_jupusdt",
    "e_kasusdt",
    "e_kavausdt",
    "e_keyusdt",
    "e_klayusdt",
    "e_kncusdt",
    "e_ksmusdt",
    "e_ldousdt",
    "e_leverusdt",
    "e_linausdt",
    "e_linkusd",
    "e_linkusdc",
    "e_linkusdt",
    "e_litusdt",
    "e_loomusdt",
    "e_lptusdt",
    "e_lqtyusdt",
    "e_lrcusdt",
    "e_lskusdt",
    "e_ltcusd",
    "e_ltcusdt",
    "e_lunausdt",
    "e_magicusdt",
    "e_manausd",
    "e_manausdc",
    "e_manausdt",
    "e_mantausdt",
    "e_maskusdt",
    "e_maticusd",
    "e_maticusdt",
    "e_maviausdt",
    "e_mavusdt",
    "e_mblusdt",
    "e_mdtusdt",
    "e_memeusdt",
    "e_metisusdt",
    "e_minausdt",
    "e_mkrusdt",
    "e_movrusdt",
    "e_mtlusdt",
    "e_myrousdt",
    "e_nearusd",
    "e_nearusdt",
    "e_neousdt",
    "e_nfpusdt",
    "e_nknusdt",
    "e_nmrusdt",
    "e_notusdt",
    "e_ntrnusdt",
    "e_oceanusdt",
    "e_ognusdt",
    "e_omgusdt",
    "e_omniusdt",
    "e_omusdt",
    "e_ondousdt",
    "e_oneusdt",
    "e_ongusdt",
    "e_ontusdt",
    "e_opusd",
    "e_opusdt",
    "e_orbsusdt",
    "e_ordiusdc",
    "e_ordiusdt",
    "e_oxtusdt",
    "e_pendleusdt",
    "e_peopleusdt",
    "e_perpusdt",
    "e_phbusdt",
    "e_pixelusdt",
    "e_polyxusdt",
    "e_portalusdt",
    "e_powrusdt",
    "e_pythusdt",
    "e_qntusdt",
    "e_qtumusdt",
    "e_racausdt",
    "e_radusdt",
    "e_rdntusdt",
    "e_reefusdt",
    "e_renusdt",
    "e_rezusdt",
    "e_rifusdt",
    "e_rlcusdt",
    "e_rndrusdt",
    "e_roninusdt",
    "e_ronusdt",
    "e_roseusdt",
    "e_rsrusdt",
    "e_runeusdt",
    "e_rvnusdt",
    "e_sagausdt",
    "e_sandusd",
    "e_sandusdt",
    "e_seiusdt",
    "e_sfpusdt",
    "e_sklusdt",
    "e_sntusdt",
    "e_snxusdt",
    "e_solusd",
    "e_solusdc",
    "e_solusdt",
    "e_spellusdt",
    "e_ssvusdt",
    "e_steemusdt",
    "e_stgusdt",
    "e_stmxusdt",
    "e_storjusdt",
    "e_stptusdt",
    "e_straxusdt",
    "e_strkusdt",
    "e_stxusdt",
    "e_suiusdc",
    "e_suiusdt",
    "e_superusdt",
    "e_sushiusdt",
    "e_sxpusdt",
    "e_taousdt",
    "e_thetausd",
    "e_thetausdt",
    "e_tiausdt",
    "e_tlmusdt",
    "e_tnsrusdt",
    "e_tokenusdt",
    "e_tonusdt",
    "e_trbusdt",
    "e_truusdt",
    "e_trxusd",
    "e_trxusdt",
    "e_turbousdt",
    "e_tusdt",
    "e_twtusdt",
    "e_umausdt",
    "e_unfiusdt",
    "e_uniusdt",
    "e_usdcusdt",
    "e_ustcusdt",
    "e_vanryusdt",
    "e_vetusdt",
    "e_vrausdt",
    "e_wavesusdt",
    "e_waxpusdt",
    "e_wifusdt",
    "e_wldusdt",
    "e_woousdt",
    "e_wsmusdt",
    "e_wusdt",
    "e_xaiusdt",
    "e_xdcusdt",
    "e_xemusdt",
    "e_xlmusd",
    "e_xlmusdt",
    "e_xmrusdt",
    "e_xrpusd",
    "e_xrpusdc",
    "e_xrpusdt",
    "e_xtzusdt",
    "e_xvgusdt",
    "e_xvsusdt",
    "e_yfiusdt",
    "e_yggusdt",
    "e_zecusdt",
    "e_zenusdt",
    "e_zetausdt",
    "e_zilusdt",
    "e_zrxusdt",
]
ws_pairs_uni = sorted([pair.replace('e_', '').upper() for pair in ws_pairs]) # 'e_btcusdt' -> 'BTCUSDT'
# %%

print(len(public_info__all_symbols))
print(len(ws_pairs))
# %%

print(public_info__all_symbols_uni[:10])
print(ws_pairs_uni[:10])
#%%
print("1-2:", set(public_info__all_symbols_uni) - set(ws_pairs_uni))
print("2-1:", set(ws_pairs_uni) - set(public_info__all_symbols_uni))
# %%
def prepare_1(item):
    return item.
# %%
import multiprocessing
import sys
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, wait
from datetime import datetime, timedelta
from time import sleep

from typing_extensions import Optional

sys.path.insert(0, "/Users/philip/Documents/projects/yarik/crypto_price_scraper/")
# %%
import json
from collections import Counter
from itertools import chain

from typing_extensions import List, Mapping
from websocket import create_connection

from src.services.lbank.types_ import WSData, WSMarketDataOverView, WSScrapingResult
from src.services.scrapers_exp.htx.test_ungzip import ungzip_bytes_to_text
from src.utils.utils import split_list, timeit_context

# %%
ws = create_connection("wss://lbkperpws.lbank.com/ws?version=1.0.0")

ws.send(
    '{"SendTopicAction":{"Action":"1","LocalNo":100,"TopicID":"7","FilterValue":"Exchange_BTCUSDT","ResumeNo":-1}}'
)


for i in range(5):
    msg = json.loads(ws.recv())
    print(msg)
    if i == 10:
        ws.send(
            '{"SendTopicAction":{"Action":"0","LocalNo":100,"TopicID":"7","FilterValue":"Exchange_BTCUSDT","ResumeNo":-1}}'
        )

    # if msg["action"] == "PushMarketDataOverView":
    #     break
# print(msg["result"][0]["data"]["UnderlyingPrice"])  # index price (maybe)
# %%
ws.close()
# %%
msg["result"]["data"]  # ['UnderlyingPrice']
# %%
all_pairs = [
    "BTCUSDT",
    "ETHUSDT",
    "APEUSDT",
    "GMTUSDT",
    "XRPUSDT",
    "DOGEUSDT",
    "MATICUSDT",
    "ADAUSDT",
    "FTMUSDT",
    "SOLUSDT",
    "RATSUSDT",
    "SATSUSDT",
    "GALAUSDT",
    "ETCUSDT",
    "ATOMUSDT",
    "BRETTUSDT",
    "WUSDT",
    "SLERFUSDT",
    "LUNAUSDT",
    "DYMUSDT",
    "ZKFUSDT",
    "TUSDT",
    "BEAMXUSDT",
    "BRC20USDT",
    "TONUSDT",
    "DOGUSDT",
    "NOTUSDT",
    "ANDYUSDT",
    "WIFUSDT",
    "TURBOUSDT",
    "MAGAUSDT",
    "KITTYUSDT",
    "CRODIEUSDT",
    "MICHIUSDT",
    "GMEUSDT",
    "BBUSDT",
    "ZEROUSDT",
    "PITUSDT",
    "XECUSDT",
    "REZUSDT",
    "ZETAUSDT",
    "MNTUSDT",
    "COREUSDT",
    "GLMUSDT",
    "ONDOUSDT",
    "OMNIUSDT",
    "TAOUSDT",
    "ZEUSUSDT",
    "SAGAUSDT",
    "TNSRUSDT",
    "ENAUSDT",
    "MEWUSDT",
    "USTCUSDT",
    "DEGENUSDT",
    "ZKUSDT",
    "BONEUSDT",
    "ETHFIUSDT",
    "BODENUSDT",
    "BOMEUSDT",
    "SCAUSDT",
    "GPUUSDT",
    "ZRXUSDT",
    "CKBUSDT",
    "MYROUSDT",
    "AXLUSDT",
    "PORTALUSDT",
    "MAVIAUSDT",
    "ALTUSDT",
    "STRKUSDT",
    "PIXELUSDT",
    "PANDORAUSDT",
    "PORKUSDT",
    "JUPUSDT",
    "WENUSDT",
    "MANTAUSDT",
    "SAVMUSDT",
    "SMILEYUSDT",
    "TROLLUSDT",
    "AVAVUSDT",
    "XAIUSDT",
    "AIUSDT",
    "METISUSDT",
    "NFPUSDT",
    "1CATUSDT",
    "KSMUSDT",
    "FETUSDT",
    "IOTAUSDT",
    "1000LUNCUSDT",
    "ETHWUSDT",
    "AUCTIONUSDT",
    "MOVRUSDT",
    "BONKUSDT",
    "SUPERUSDT",
    "GROKUSDT",
    "PYTHUSDT",
    "XTZUSDT",
    "OMUSDT",
    "ALICEUSDT",
    "SILLYUSDT",
    "CHZUSDT",
    "HBARUSDT",
    "HOTUSDT",
    "CHRUSDT",
    "EGLDUSDT",
    "BSSBUSDT",
    "JTOUSDT",
    "FTTUSDT",
    "THETAUSDT",
    "TLMUSDT",
    "ONTUSDT",
    "CELRUSDT",
    "ONEUSDT",
    "ALGOUSDT",
    "KLAYUSDT",
    "DARUSDT",
    "GALUSDT",
    "JOEUSDT",
    "NKNUSDT",
    "RVNUSDT",
    "ACEUSDT",
    "TURTUSDT",
    "MUBIUSDT",
    "CSPRUSDT",
    "VANRYUSDT",
    "BADGERUSDT",
    "OCEANUSDT",
    "ARUSDT",
    "TOKENUSDT",
    "TIAUSDT",
    "CAKEUSDT",
    "WOJAKUSDT",
    "IOTXUSDT",
    "RLBUSDT",
    "STEEMUSDT",
    "API3USDT",
    "SNTUSDT",
    "MEMECOINUSDT",
    "SUSHIUSDT",
    "NEOUSDT",
    "QNTUSDT",
    "GMXUSDT",
    "HIFIUSDT",
    "OPUSDT",
    "PEPEUSDT",
    "SHIBUSDT",
    "NEARUSDT",
    "LTCUSDT",
    "LINKUSDT",
    "FILUSDT",
    "BCHUSDT",
    "BNBUSDT",
    "ARBUSDT",
    "NMRUSDT",
    "APTUSDT",
    "LINAUSDT",
    "LEVERUSDT",
    "TRBUSDT",
    "MINAUSDT",
    "PEOPLEUSDT",
    "ALPHAUSDT",
    "ARKUSDT",
    "FLMUSDT",
    "GTCUSDT",
    "VETUSDT",
    "ICPUSDT",
    "EOSUSDT",
    "GRTUSDT",
    "COMPUSDT",
    "WOOUSDT",
    "LITUSDT",
    "XVSUSDT",
    "BAKEUSDT",
    "LPTUSDT",
    "ENJUSDT",
    "AVAXUSDT",
    "UMAUSDT",
    "STORJUSDT",
    "XVGUSDT",
    "MAVUSDT",
    "SFPUSDT",
    "ORDIUSDT",
    "AAVEUSDT",
    "AIDOGEUSDT",
    "BLZUSDT",
    "MKRUSDT",
    "KEYUSDT",
    "SNXUSDT",
    "1INCHUSDT",
    "TRXUSDT",
    "XEMUSDT",
    "RNDRUSDT",
    "MASKUSDT",
    "IDUSDT",
    "AGIXUSDT",
    "CFXUSDT",
    "MANAUSDT",
    "FLOKIUSDT",
    "DYDXUSDT",
    "WAVESUSDT",
    "HIGHUSDT",
    "HOOKUSDT",
    "MAGICUSDT",
    "BITCOINUSDT",
    "LDOUSDT",
    "SUIUSDT",
    "UNIUSDT",
    "LQTYUSDT",
    "BIGTIMEUSDT",
    "KAVAUSDT",
    "WLDUSDT",
    "POLYXUSDT",
    "INJUSDT",
    "LRCUSDT",
    "FRONTUSDT",
    "GASUSDT",
    "ROSEUSDT",
    "RIFUSDT",
    "STXUSDT",
    "BICOUSDT",
    "RUNEUSDT",
    "BONDUSDT",
    "LADYSUSDT",
    "RDNTUSDT",
    "SXPUSDT",
    "BNXUSDT",
    "OMGUSDT",
    "KNCUSDT",
    "RLCUSDT",
    "KASUSDT",
    "PEPE2USDT",
    "IOSTUSDT",
    "ARKMUSDT",
    "TIPUSDT",
    "IMXUSDT",
    "AXSUSDT",
    "PENDLEUSDT",
    "FLOWUSDT",
    "RENUSDT",
    "ENSUSDT",
    "BSVUSDT",
    "XENUSDT",
    "CELOUSDT",
    "COMBOUSDT",
    "SANDUSDT",
    "BLURUSDT",
    "XLMUSDT",
    "DOTUSDT",
    "C98USDT",
    "POWRUSDT",
    "BELUSDT",
    "YGGUSDT",
    "ARPAUSDT",
    "STARLUSDT",
    "JASMYUSDT",
    "DODOUSDT",
    "SSVUSDT",
    "SEIUSDT",
]


# %%
def scrape_all_parallel(all_pairs: List[str]) -> List[WSScrapingResult]:
    # open ws
    # for each pair send subscription request
    # each result - look at those that are of interest
    #   - populate dict with results as new messages arrive
    # either i populated all dict fields or timeout exceeded
    #   each time I add value - i update set - i want that set to be same as set of all keys
    #   after 10 secs i return dict however populated it is
    #     i might also want to log what fields were not populated
    #       for some symbols server might return error/no success subscribe message that I might want to handle it not to wait for those symbols or just embrace timeout

    scraping_results: Mapping[str, WSScrapingResult] = {}

    def check_all_scraped():
        "Returns True if all pairs have been scraped (have entry in scraping_results dict)"
        if len(set(all_pairs) - set(scraping_results.keys())) == 0:
            return True
        return False

    def check_timeout():
        return datetime.now() > should_finish_before

    def handle_incoming_ws_event(event: WSMarketDataOverView):
        if "requestNo" in event:
            nonlocal scraping_results
            symbol = event["result"][0]["data"]["ExchangeID"]
            scraping_results[symbol] = {
                "symbol": symbol,
                "data_point": event["result"][0]["data"],
            }

    should_finish_before = datetime.now() + timedelta(seconds=10)  # for timeout
    should_finish = False  # flip when time to finish (timeout)
    ws = create_connection("wss://lbkperpws.lbank.com/ws?version=1.0.0")

    ws.send(
        '{"SendTopicAction":{"Action":"1","LocalNo":100,"TopicID":"7","FilterValue":"Exchange_BTCUSDT","ResumeNo":-1}}'
    )
    while True:
        ws.recv()
        sleep(0.1)
    return scraping_results


# %%
def scrape_symbols_sequential(symbols: List[str]) -> List[WSScrapingResult]:
    scraping_results: List[WSScrapingResult] = []

    ws = create_connection("wss://lbkperpws.lbank.com/ws?version=1.0.0")
    with timeit_context("sequential prices"):
        for symbol in symbols:
            print("wanna send")
            print("wanna send")
            ws.send(
                '{"SendTopicAction":{"Action":"1","LocalNo":100,"TopicID":"7","FilterValue":"Exchange_%s","ResumeNo":-1}}'
                % symbol
            )
            for i in range(5):
                msg: WSMarketDataOverView = json.loads(
                    ws.recv()
                )  # actually can be different type, next line chekcs it
                print(msg)
                if (
                    msg["action"] == "PushMarketDataOverView"
                    and "requestNo" in msg
                    and symbol == msg["result"][0]["data"]["InstrumentID"]
                ):
                    scraping_results.append(
                        {
                            "symbol": symbol,
                            "data_point": msg["result"][0]["data"],
                        }
                    )
                    break
            else:
                print(f"oops.. symbol: {symbol}")
                scraping_results.append(
                    {
                        "symbol": symbol,
                        "data_point": None,
                    }
                )
            ws.send(
                '{"SendTopicAction":{"Action":"0","LocalNo":100,"TopicID":"7","FilterValue":"Exchange_%s","ResumeNo":-1}}'
                % symbol
            )

    return scraping_results


# %%
def parallelized_sequential_scrape(all_pairs: List[str]):
    parallelization_limit = 4

    task_groups = split_list(all_pairs, parallelization_limit)

    with ThreadPoolExecutor(max_workers=parallelization_limit) as executor:
        # with ProcessPoolExecutor(max_workers=parallelization_limit) as executor:
        futures = [
            executor.submit(scrape_symbols_sequential, task_group)
            for task_group in task_groups
        ]
        results = [future.result() for future in futures]

    return results

    # with multiprocessing.Pool(parallelization_limit) as pool:
    #     results = pool.map(scrape_symbols_sequential, task_groups)
    # return results


# %%
# scrape_symbols_sequential(all_pairs[: int(len(all_pairs) * 1)])
scraped = parallelized_sequential_scrape(all_pairs)
# %%
scraped
# %%

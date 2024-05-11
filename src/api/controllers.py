import csv
import io

import httpx
from fastapi import APIRouter, Body, Depends, Query, Request
from fastapi.responses import StreamingResponse
from typing_extensions import Annotated, List, Optional

from src.api.templates import templates
from src.config import config
from src.db.repositories.mexc.TickerTimeseries import get_ticker_timeseries
from src.services.scrapers.mexc.checks_notifications import (
    fire_notification_1,
    fire_notification_2,
    fire_notification_3,
)
from src.services.scrapers.mexc.get_ticker_data import get_ticker_data, get_tickers_data
from src.services.scrapers.mexc.get_ticker_short_data import (
    get_ticker_short_data,
    get_tickers_short_data,
)

router = APIRouter()


@router.get("/scrape/{symbol}")
async def scrape_symbol(symbol: str):
    return get_ticker_data(symbol)


@router.get("/scrape")
async def scrape_all():
    return get_tickers_data()


@router.get("/scrape_short/{symbol}")
async def scrape_symbol_short(symbol: str):
    return get_ticker_short_data(symbol)


@router.get("/scrape_short")
async def scrape_all_short():
    return get_tickers_short_data()


@router.get("/pairs")
async def register_session():
    return [
        "100000AIDOGE_USDT",
        "10000COQ_USDT",
        "10000LADYS_USDT",
        "10000WEN_USDT",
        "1000BONK_USDT",
        "1000BTT_USDT",
        "1000IQ50_USDT",
        "1000RATS_USDT",
        "1000STARL_USDT",
        "1CAT_USDT",
        "1INCH_USDT",
        "AAVE_USDT",
        "ACE_USDT",
        "ACH_USDT",
        "ADA_USDT",
        "AERGO_USDT",
        "AEVO_USDT",
        "AGIX_USDT",
        "AGI_USDT",
        "AGLD_USDT",
        "AI_USDT",
        "AKRO_USDT",
        "ALGO_USDT",
        "ALICE_USDT",
        "ALPACA_USDT",
        "ALPHA_USDT",
        "ALT_USDT",
        "AMB_USDT",
        "ANKR_USDT",
        "ANT_USDT",
        "APE_USDT",
        "API3_USDT",
        "APT_USDT",
        "ARB_USDT",
        "ARKM_USDT",
        "ARK_USDT",
        "ARPA_USDT",
        "AR_USDT",
        "ASTR_USDT",
        "ATA_USDT",
        "ATOM_USDT",
        "AUCTION_USDT",
        "AUDIO_USDT",
        "AVAX_USDT",
        "AXL_USDT",
        "AXS_USDT",
        "BADGER_USDT",
        "BAKE_USDT",
        "BAL_USDT",
        "BAND_USDT",
        "BAT_USDT",
        "BCH_USDT",
        "BEAMX_USDT",
        "BEL_USDT",
        "BICO_USDT",
        "BIGTIME_USDT",
        "BLOCK_USDT",
        "BLUR_USDT",
        "BLZ_USDT",
        "BNB_USDT",
        "BNT_USDT",
        "BNXNEW_USDT",
        "BOBA_USDT",
        "BOME_USDT",
        "BOND_USDT",
        "BONE_USDT",
        "BRETT_USDT",
        "BSV_USDT",
        "BSW_USDT",
        "BTC_USD",
        "BTC_USDT",
        "C98_USDT",
        "CAKE_USDT",
        "CEEK_USDT",
        "CELO_USDT",
        "CELR_USDT",
        "CEL_USDT",
        "CETUS_USDT",
        "CFX_USDT",
        "CHR_USDT",
        "CHZ_USDT",
        "CKB_USDT",
        "COMBO_USDT",
        "COMP_USDT",
        "CORE_USDT",
        "COTI_USDT",
        "CRO_USDT",
        "CRV_USDT",
        "CSPR_USDT",
        "CTC_USDT",
        "CTK_USDT",
        "CTSI_USDT",
        "CVC_USDT",
        "CVX_USDT",
        "CYBER_USDT",
        "DAO_USDT",
        "DAR_USDT",
        "DASH_USDT",
        "DATA_USDT",
        "DEGEN_USDT",
        "DENT_USDT",
        "DGB_USDT",
        "DMAIL_USDT",
        "DODO_USDT",
        "DOGE_USDT",
        "DOT_USDT",
        "DUSK_USDT",
        "DYDX_USDT",
        "DYM_USDT",
        "EDU_USDT",
        "EGLD_USDT",
        "ENA_USDT",
        "ENJ_USDT",
        "ENS_USDT",
        "EOS_USDT",
        "ETC_USDT",
        "ETHFI_USDT",
        "ETHW_USDT",
        "ETH_USD",
        "ETH_USDT",
        "FET_USDT",
        "FILECOIN_USDT",
        "FITFI_USDT",
        "FLM_USDT",
        "FLOKI_USDT",
        "FLOW_USDT",
        "FLR_USDT",
        "FORTH_USDT",
        "FOXY_USDT",
        "FRONT_USDT",
        "FTM_USDT",
        "FTT_USDT",
        "FUN_USDT",
        "FXS_USDT",
        "GALA_USDT",
        "GAL_USDT",
        "GAS_USDT",
        "GFT_USDT",
        "GLMR_USDT",
        "GLM_USDT",
        "GMT_USDT",
        "GMX_USDT",
        "GODS_USDT",
        "GROK_USDT",
        "GRT_USDT",
        "GTC_USDT",
        "HBAR_USDT",
        "HFT_USDT",
        "HIFI_USDT",
        "HIGH_USDT",
        "HNT_USDT",
        "HOOK_USDT",
        "HOT_USDT",
        "ICP_USDT",
        "ICX_USDT",
        "IDEX_USDT",
        "ID_USDT",
        "ILV_USDT",
        "IMX_USDT",
        "INJ_USDT",
        "IOST_USDT",
        "IOTA_USDT",
        "IOTX_USDT",
        "JASMY_USDT",
        "JOE_USDT",
        "JTO_USDT",
        "JUP_USDT",
        "KAS_USDT",
        "KAVA_USDT",
        "KDA_USDT",
        "KEY_USDT",
        "KLAY_USDT",
        "KNC_USDT",
        "KSM_USDT",
        "LAI_USDT",
        "LDO_USDT",
        "LEVER_USDT",
        "LINA_USDT",
        "LINK_USDT",
        "LIT_USDT",
        "LOOKS_USDT",
        "LOOM_USDT",
        "LPT_USDT",
        "LQTY_USDT",
        "LRC_USDT",
        "LSK_USDT",
        "LTC_USDT",
        "LTO_USDT",
        "LUNANEW_USDT",
        "LUNC_USDT",
        "MAGIC_USDT",
        "MANA_USDT",
        "MANTA_USDT",
        "MASK_USDT",
        "MATIC_USDT",
        "MAVIA_USDT",
        "MAV_USDT",
        "MBL_USDT",
        "MDT_USDT",
        "MEME_USDT",
        "MERL_USDT",
        "METIS_USDT",
        "MEW_USDT",
        "MINA_USDT",
        "MKR_USDT",
        "MNT_USDT",
        "MOBILE_USDT",
        "MOVR_USDT",
        "MSN_USDT",
        "MTL_USDT",
        "MUBI_USDT",
        "MYRO_USDT",
        "NEAR_USDT",
        "NEO_USDT",
        "NFP_USDT",
        "NKN_USDT",
        "NMR_USDT",
        "NTRN_USDT",
        "OCEAN_USDT",
        "OGN_USDT",
        "OMG_USDT",
        "OMNI_USDT",
        "OM_USDT",
        "ONDO_USDT",
        "ONE_USDT",
        "ONG_USDT",
        "ONT_USDT",
        "OP_USDT",
        "ORBS_USDT",
        "ORDI_USDT",
        "ORN_USDT",
        "OXT_USDT",
        "PAXG_USDT",
        "PENDLE_USDT",
        "PEOPLE_USDT",
        "PEPECOMMUNITY_USDT",
        "PEPE_USDT",
        "PERP_USDT",
        "PHB_USDT",
        "PIXEL_USDT",
        "POLYX_USDT",
        "POPCAT_USDT",
        "PORTAL_USDT",
        "POWR_USDT",
        "PRCL_USDT",
        "PROM_USDT",
        "PUNDU_USDT",
        "PYTH_USDT",
        "QI_USDT",
        "QNT_USDT",
        "QTUM_USDT",
        "RAD_USDT",
        "RARE_USDT",
        "RAY_USDT",
        "RDNT_USDT",
        "REEF_USDT",
        "REN_USDT",
        "REQ_USDT",
        "REZ_USDT",
        "RIF_USDT",
        "RLC_USDT",
        "RNDR_USDT",
        "RON_USDT",
        "ROSE_USDT",
        "RPL_USDT",
        "RSR_USDT",
        "RSS3_USDT",
        "RUNE_USDT",
        "RVN_USDT",
        "SAFE_USDT",
        "SAGA_USDT",
        "SAND_USDT",
        "SATS_USDT",
        "SCA_USDT",
        "SCRT_USDT",
        "SC_USDT",
        "SEI_USDT",
        "SFP_USDT",
        "SHIB_USDT",
        "SILLY_USDT",
        "SKL_USDT",
        "SLERF_USDT",
        "SLP_USDT",
        "SNT_USDT",
        "SNX_USDT",
        "SOL_USDT",
        "SPELL_USDT",
        "SSV_USDT",
        "STEEM_USDT",
        "STG_USDT",
        "STMX_USDT",
        "STORJ_USDT",
        "STPT_USDT",
        "STRK_USDT",
        "STX_USDT",
        "SUI_USDT",
        "SUN_USDT",
        "SUPER_USDT",
        "SUSHI_USDT",
        "SWEAT_USDT",
        "SXP_USDT",
        "TAO_USDT",
        "THETA_USDT",
        "TIA_USDT",
        "TLM_USDT",
        "TNSR_USDT",
        "TOKEN_USDT",
        "TOMI_USDT",
        "TONCOIN_USDT",
        "TRB_USDT",
        "TRU_USDT",
        "TRX_USDT",
        "TURBO_USDT",
        "TWT_USDT",
        "T_USDT",
        "UMA_USDT",
        "UNFI_USDT",
        "UNI_USDT",
        "USDC_USDT",
        "USTC_USDT",
        "VANRY_USDT",
        "VELO_USDT",
        "VET_USDT",
        "VRA_USDT",
        "VTHO_USDT",
        "WAVES_USDT",
        "WAXP_USDT",
        "WIF_USDT",
        "WLD_USDT",
        "WOO_USDT",
        "W_USDT",
        "XAI_USDT",
        "XCH_USDT",
        "XCN_USDT",
        "XEC_USDT",
        "XEM_USDT",
        "XLM_USDT",
        "XMR_USDT",
        "XNO_USDT",
        "XRD_USDT",
        "XRP_USDT",
        "XTZ_USDT",
        "XVG_USDT",
        "XVS_USDT",
        "YFI_USDT",
        "YGG_USDT",
        "ZBCN_USDT",
        "ZEC_USDT",
        "ZEN_USDT",
        "ZERO_USDT",
        "ZETA_USDT",
        "ZEUS_USDT",
        "ZIL_USDT",
        "ZKF_USDT",
        "ZK_USDT",
        "ZRX_USDT",
    ]


@router.get("/n_last_ticks")
async def n_last_ticks(symbol: str, n: int):
    return get_ticker_timeseries(symbol, steps=n)


@router.get("/n_last_ticks_table")
async def n_last_ticks_table(request: Request, symbol: str, n: int):
    data_points = get_ticker_timeseries(symbol, steps=n)
    return templates.TemplateResponse(
        request=request, name="table.html", context={"data_points": data_points}
    )


@router.get("/n_last_ticks_csv")
async def n_last_ticks_csv(symbol: str, n: int):
    data = get_ticker_timeseries(symbol, steps=n)

    # Create a string buffer to store the CSV data
    buffer = io.StringIO()

    # Initialize a CSV DictWriter
    fieldnames = [
        "symbol",
        "timestamp",
        "last_price",
        "fair_price",
        "last_div_fair",
        "delta_div_avg",
    ]
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)

    # Write the header and rows to the buffer
    writer.writeheader()
    writer.writerows(data)

    # Move the buffer's position to the beginning
    buffer.seek(0)

    # Return the buffer data as a streaming response
    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=ticker_timeseries.csv"},
    )


@router.get("/send_test_broadcast_notif")
async def send_test_broadcast_notif():
    # fire_notification_1()
    # fire_notification_2()
    fire_notification_3()


@router.get("/send_test_notif")
async def send_test_notif(chat_id: int):
    message = """
BTC is going crazy!

https://futures.mexc.com/ru-RU/exchange/BTC_USDT

<link to table with last n steps>
"""
    payload = {
        "chat_id": chat_id,
        "text": message,
    }
    httpx.post(f"{config['telegram_bot_api_base_url']}/sendMessage", json=payload)

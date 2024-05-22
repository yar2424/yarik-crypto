import csv
import io

import httpx
from fastapi import APIRouter, Body, Depends, Query, Request
from fastapi.responses import StreamingResponse
from typing_extensions import Annotated, List, Optional

from src.api.templates import templates
from src.config import config
from src.db.repositories.mexc.TickerTimeseries import get_ticker_timeseries
from src.services.mexc.scrape.get_ticker_data import get_ticker_data, get_tickers_data
from src.services.mexc.scrape.get_ticker_short_data import (
    get_ticker_short_data,
    get_tickers_short_data,
)
from src.utils.telegram import send_message_broadcast

router = APIRouter()


@router.get("/scrape/{symbol}", tags=["mexc"])
async def scrape_symbol(symbol: str):
    return get_ticker_data(symbol)


@router.get("/scrape", tags=["mexc"])
async def scrape_all():
    return get_tickers_data()


@router.get("/scrape_short/{symbol}", tags=["mexc"])
async def scrape_symbol_short(symbol: str):
    return get_ticker_short_data(symbol)


@router.get("/scrape_short", tags=["mexc"])
async def scrape_all_short():
    return get_tickers_short_data()


@router.get("/pairs", tags=["mexc"])
async def register_session():
    all_tickers = get_tickers_data()
    all_symbols = sorted([ticker["symbol"] for ticker in all_tickers])
    return all_symbols


@router.get("/n_last_ticks", tags=["mexc"])
async def n_last_ticks(symbol: str, n: int):
    return get_ticker_timeseries(symbol, steps=n)


@router.get("/n_last_ticks_table", tags=["mexc"])
async def n_last_ticks_table(request: Request, symbol: str, n: int):
    data_points = get_ticker_timeseries(symbol, steps=n)
    return templates.TemplateResponse(
        request=request,
        name="table.html",
        context={
            "text_columns": [
                "symbol",
                "timestamp",
            ],
            "numeric_columns": [
                "last_price",
                "fair_price",
                "index_price",
                "funding_rate",
                "index_fair_delta_div_index",
                "fair_last_delta_div_fair",
                "last_fair_delta_div_avg",
            ],
            "data_points": data_points,
        },
    )


@router.get("/n_last_ticks_csv", tags=["mexc"])
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
        "index_price",
        "funding_rate",
        #
        "index_fair_delta_div_index",
        "fair_last_delta_div_fair",
        #
        "last_fair_delta_div_avg",
    ]
    # fieldnames = list(data[0].keys())
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

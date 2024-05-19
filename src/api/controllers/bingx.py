import csv
import io

import httpx
from fastapi import APIRouter, Body, Depends, Query, Request
from fastapi.responses import StreamingResponse
from typing_extensions import Annotated, List, Optional

from src.api.templates import templates
from src.config import config
from src.db.repositories.bingx.TickerTimeseries import get_ticker_timeseries
from src.services.bingx.all_symbols import all_symbols
from src.services.bingx.scrape.get_ticker_data import get_ticker_data, get_tickers_data
from src.utils.telegram import send_message_broadcast

router = APIRouter()


@router.get("/scrape/{symbol}", tags=["bingx"])
async def scrape_symbol(symbol: str):
    return await get_ticker_data(symbol)


@router.get("/scrape", tags=["bingx"])
async def scrape_all():
    return await get_tickers_data()


@router.get("/pairs", tags=["bingx"])
async def register_session():
    return all_symbols


@router.get("/n_last_ticks", tags=["bingx"])
async def n_last_ticks(symbol: str, n: int):
    return get_ticker_timeseries(symbol, steps=n)


@router.get("/n_last_ticks_table", tags=["bingx"])
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
                "trade_price",
                "fair_price",
                "index_price",
                "funding_rate",
                "index_fair_delta_div_index",
                "fair_trade_delta_div_fair",
            ],
            "data_points": data_points,
        },
    )


@router.get("/n_last_ticks_csv", tags=["bingx"])
async def n_last_ticks_csv(symbol: str, n: int):
    data = get_ticker_timeseries(symbol, steps=n)

    # Create a string buffer to store the CSV data
    buffer = io.StringIO()

    # Initialize a CSV DictWriter
    fieldnames = [
        "symbol",
        "timestamp",
        "trade_price",
        "fair_price",
        "index_price",
        "funding_rate" "index_fair_delta_div_index",
        "fair_trade_delta_div_fair",
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
import csv
import io

import httpx
from fastapi import APIRouter, Body, Depends, Query, Request
from fastapi.responses import StreamingResponse
from typing_extensions import Annotated, List, Optional

from src.api.templates import templates
from src.config import config
from src.db.repositories.phemex.TickerTimeseries import get_ticker_timeseries
from src.services.phemex.scrape.get_ticker_data import get_all_symbols, get_tickers_data
from src.utils.telegram import send_message_broadcast

router = APIRouter()


# @router.get("/scrape/{symbol}", tags=["phemex"])
# async def scrape_symbol(symbol: str):
#     return await get_ticker_data(symbol)


@router.get("/scrape", tags=["phemex"])
async def scrape_all():
    return await get_tickers_data()


@router.get("/pairs", tags=["phemex"])
async def register_session():
    all_symbols = get_all_symbols()
    return all_symbols


@router.get("/n_last_ticks", tags=["phemex"])
async def n_last_ticks(symbol: str, n: int):
    return get_ticker_timeseries(symbol, steps=n)


@router.get("/n_last_ticks_table", tags=["phemex"])
async def n_last_ticks_table(request: Request, symbol: str, n: int):
    data_points = get_ticker_timeseries(symbol, steps=n)
    pretty_data_points = [
        {**data_point, "n": str(idx + 1), "timestamp": data_point["timestamp"][:-10]}
        for idx, data_point in enumerate(data_points)
    ]
    return templates.TemplateResponse(
        request=request,
        name="table.html",
        context={
            "text_columns": [
                "n",
                "symbol",
                "timestamp",
            ],
            "numeric_columns": [
                "last_price",
                "mark_price",
                "index_price",
                "funding_rate",
                "index_mark_delta_div_index",
                "mark_last_delta_div_mark",
            ],
            "data_points": pretty_data_points,
        },
    )


@router.get("/n_last_ticks_csv", tags=["phemex"])
async def n_last_ticks_csv(symbol: str, n: int):
    data = get_ticker_timeseries(symbol, steps=n)

    # Create a string buffer to store the CSV data
    buffer = io.StringIO()

    # Initialize a CSV DictWriter
    fieldnames = [
        "symbol",
        "timestamp",
        "last_price",
        "mark_price",
        "index_price",
        "funding_rate",
        #
        "index_mark_delta_div_index",
        "mark_last_delta_div_mark",
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

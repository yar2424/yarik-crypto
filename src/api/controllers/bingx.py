import csv
import io

import httpx
from fastapi import APIRouter, Body, Depends, Query, Request
from fastapi.responses import StreamingResponse
from typing_extensions import Annotated, List, Optional

from src.api.templates import templates
from src.config import config
from src.db.repositories.bingx.TickerTimeseries import get_ticker_timeseries
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
    all_tickers = await get_tickers_data()
    all_symbols = sorted([ticker["symbol"] for ticker in all_tickers])
    return all_symbols


@router.get("/n_last_ticks", tags=["bingx"])
async def n_last_ticks(symbol: str, n: int):
    return reversed(get_ticker_timeseries(symbol, steps=n))


@router.get("/n_last_ticks_table", tags=["bingx"])
async def n_last_ticks_table(request: Request, symbol: str, n: int):
    data_points = reversed(get_ticker_timeseries(symbol, steps=n))
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
                "trade_price",
                "fair_price",
                "index_price",
                "funding_rate",
                "index_fair_delta_div_index",
                "fair_trade_delta_div_fair",
            ],
            "data_points": pretty_data_points,
        },
    )


@router.get("/n_last_ticks_csv", tags=["bingx"])
async def n_last_ticks_csv(symbol: str, n: int):
    data = reversed(get_ticker_timeseries(symbol, steps=n))

    # Create a string buffer to store the CSV data
    buffer = io.StringIO()

    # Initialize a CSV DictWriter
    fieldnames = [
        "symbol",
        "timestamp",
        "trade_price",
        "fair_price",
        "index_price",
        "funding_rate",
        #
        "index_fair_delta_div_index",
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

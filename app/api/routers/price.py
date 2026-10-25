import re

from fastapi import APIRouter, HTTPException
from app.core.price import get_price_history
from app.data.price.twelvedata_client import TwelveData
from app.schemas.price_response import PriceResponse

router = APIRouter()

TICKER_PATTERN = re.compile(r"^[A-Z]{1,5}$")

@router.get("/price/{ticker}", response_model=PriceResponse)
def price(ticker: str):
    ticker = ticker.upper()
    if not TICKER_PATTERN.match(ticker):
        raise HTTPException(status_code=400, detail=f"Invalid ticker format: '{ticker}'")
    return get_price_history(ticker, TwelveData())
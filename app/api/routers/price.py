from fastapi import APIRouter, HTTPException
from app.core.price import get_price_history
from app.data.price.twelvedata_client import TwelveData
from app.data.price.price_fetcher import PriceHistoryError
from app.schemas.price_response import PriceResponse

router = APIRouter()

@router.get("/price/{ticker}", response_model=PriceResponse)
def price(ticker: str):
    try:
        return get_price_history(ticker.upper(), TwelveData())
    except PriceHistoryError:
        raise HTTPException(status_code=404, detail=f"No price data for '{ticker}'")
import re

from fastapi import APIRouter, HTTPException
from app.core.score_history import get_history
from app.schemas.history_response import HistoryResponse

router = APIRouter()

# regex generate by Claude AI
TICKER_PATTERN = re.compile(r"^[A-Z]{1,5}$")

@router.get("/history/{ticker}", response_model=HistoryResponse)
def history(ticker: str):
    ticker = ticker.upper()
    if not TICKER_PATTERN.match(ticker):
        raise HTTPException(status_code=400, detail=f"Invalid ticker format: '{ticker}'")
    return get_history(ticker)
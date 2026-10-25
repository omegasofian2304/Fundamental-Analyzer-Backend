import re

from fastapi import APIRouter, HTTPException
from app.core.score_calculator import get_score
from app.data.metrics.fetch_finnhub import Finnhub
from app.data.cache.cache import CachedMetricFetcher
from app.schemas.score_response import ScoreResponse

router = APIRouter()

TICKER_PATTERN = re.compile(r"^[A-Z]{1,5}$")

@router.get("/score/{ticker}", response_model=ScoreResponse)
def score(ticker: str):
    ticker = ticker.upper()
    if not TICKER_PATTERN.match(ticker):
        raise HTTPException(status_code=400, detail=f"Invalid ticker format: '{ticker}'")
    metric_client = CachedMetricFetcher(Finnhub())
    return get_score(ticker, metric_client)
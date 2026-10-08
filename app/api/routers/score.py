from fastapi import APIRouter, HTTPException
from app.core.score_calculator import get_score
from app.data.metrics.fundamental_metrics_fetcher import MetricFetchError
from app.data.metrics.fetch_finnhub import Finnhub
from app.data.cache.cache import CachedMetricFetcher
from app.schemas.score_response import ScoreResponse

router = APIRouter()

@router.get("/score/{ticker}", response_model=ScoreResponse)
def score(ticker: str):
    metric_client = CachedMetricFetcher(Finnhub())
    try:
        return get_score(ticker.upper(), metric_client)
    except MetricFetchError:
        raise HTTPException(status_code=404, detail=f"Ticker '{ticker}' not found")
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
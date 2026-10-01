import json
from datetime import datetime
from app.data.metrics.fetch_finnhub import Finnhub
from app.data.metrics.fundamental_metrics_fetcher import MetricFetcher
from app.data.redis_client import get_redis
from app.data.tickers.sp500_github_client import SP500Github

TICKERS_TTL_SECONDS = 60 * 60 * 24 * 30 * 6  # 6 months
METRICS_TTL_SECONDS = 60 * 60 * 24 * 100  # 100 days (quarterly filings + margin)
BOUNDS_TTL_SECONDS = METRICS_TTL_SECONDS  # same lifetime as the metrics they come from



def get_tickers_cached() -> list[str]:

    r = get_redis()
    key = "sp500:tickers" #to be able to save the data under this key

    cached = r.get(key)
    if cached is not None:
        return json.loads(cached)

    tickers = SP500Github().get_tickers()
    r.setex(key, TICKERS_TTL_SECONDS, json.dumps(tickers))
    return tickers



def _metrics_to_json(metrics: dict) -> dict:

    return {
        name: [(date.isoformat(), value) for date, value in points]
        for name, points in metrics.items()
    }


def _metrics_from_json(data: dict) -> dict:
    return {
        name: [(datetime.fromisoformat(date), value) for date, value in points]
        for name, points in data.items()
    }


def fetch_metric_cached(ticker: str, force_refresh: bool = False) -> dict:
    r = get_redis()
    key = f"sp500:metrics:{ticker}"

    if not force_refresh:
        cached = r.get(key)
        if cached is not None:
            return _metrics_from_json(json.loads(cached))

    metrics = Finnhub().fetch_metric(ticker)
    r.setex(key, METRICS_TTL_SECONDS, json.dumps(_metrics_to_json(metrics)))
    return metrics


class CachedMetricFetcher(MetricFetcher):


    def fetch_metric(self, ticker):
        return fetch_metric_cached(ticker)



def set_bounds_cached(bounds: dict) -> None:

    r = get_redis()

    for metric_name, (low, high) in bounds.items():
        key = f"sp500:percentile_bounds:{metric_name}"
        # float() converts numpy floats to plain Python floats
        r.setex(key, BOUNDS_TTL_SECONDS, json.dumps([float(low), float(high)]))


def get_bounds_cached(metric_names: list[str]) -> dict | None:

    r = get_redis()
    bounds = {}

    for metric_name in metric_names:
        cached = r.get(f"sp500:percentile_bounds:{metric_name}")
        if cached is None:
            return None
        bounds[metric_name] = json.loads(cached)

    return bounds


def are_bounds_fresh(metric_names: list[str]) -> bool:

    return get_bounds_cached(metric_names) is not None

import json
from datetime import datetime
from app.data.metrics.fundamental_metrics_fetcher import MetricFetcher
from app.data.cache.redis_client import get_redis

TICKERS_TTL_SECONDS = 60 * 60 * 24 * 30 * 6  # 6 months
METRICS_TTL_SECONDS = 60 * 60 * 24 * 100  # 100 days (quarterly filings + margin)
BOUNDS_TTL_SECONDS = METRICS_TTL_SECONDS  # same lifetime as the metrics they come from


def get_tickers_cached(ticker_client) -> list[str]:
    """
     Return the S&P 500 ticker list, fetching from GitHub and caching in Redis if missing
    """
    r = get_redis()
    key = "sp500:tickers"

    cached = r.get(key)
    if cached is not None:
        return json.loads(cached)

    tickers = ticker_client.get_tickers()
    r.setex(key, TICKERS_TTL_SECONDS, json.dumps(tickers))
    return tickers


def _metrics_to_json(metrics: dict) -> dict:
    """
    Convert metric dicts (datetime keys) to JSON-serializable format
    """
    return {
        name: [(date.isoformat(), value) for date, value in points]
        for name, points in metrics.items()
    }


def _metrics_from_json(data: dict) -> dict:
    """
    Restore metric dicts from their JSON-serialized format
    """
    return {
        name: [(datetime.fromisoformat(date), value) for date, value in points]
        for name, points in data.items()
    }


def cache_metrics(ticker: str, metrics: dict) -> None:
    """
    Write one ticker's fundamental metrics into Redis
    """
    r = get_redis()
    key = f"sp500:metrics:{ticker}"
    r.setex(key, METRICS_TTL_SECONDS, json.dumps(_metrics_to_json(metrics)))


def fetch_metric_cached(metric_fetcher, ticker: str, force_refresh: bool = False) -> dict:
    """
    Return cached metrics for a ticker, or fetch from Finnhub and cache the result
    """
    r = get_redis()
    key = f"sp500:metrics:{ticker}"

    if not force_refresh:
        cached = r.get(key)
        if cached is not None:
            return _metrics_from_json(json.loads(cached))

    metrics = metric_fetcher.fetch_metric(ticker)
    cache_metrics(ticker, metrics)
    return metrics


class CachedMetricFetcher(MetricFetcher):
    """
    MetricFetcher that reads through the Redis cache before hitting Finnhub
    """

    def __init__(self, metric_fetcher):
        self._fetcher = metric_fetcher

    def fetch_metric(self, ticker):
        return fetch_metric_cached(self._fetcher, ticker)


def set_bounds_cached(bounds: dict) -> None:
    """
    Store percentile bounds per metric in Redis
    """
    r = get_redis()

    for metric_name, (low, high) in bounds.items():
        key = f"sp500:percentile_bounds:{metric_name}"
        # float() converts numpy floats to plain Python floats
        r.setex(key, BOUNDS_TTL_SECONDS, json.dumps([float(low), float(high)]))


def get_bounds_cached(metric_names: list[str]) -> dict | None:
    """
    Return all cached bounds for the given metrics, or None if any is missing
    """
    r = get_redis()
    bounds = {}

    for metric_name in metric_names:
        cached = r.get(f"sp500:percentile_bounds:{metric_name}")
        if cached is None:
            return None
        bounds[metric_name] = json.loads(cached)

    return bounds


def are_bounds_fresh(metric_names: list[str]) -> bool:
    """
    Check whether all percentile bounds are still present in Redis
    """
    return get_bounds_cached(metric_names) is not None
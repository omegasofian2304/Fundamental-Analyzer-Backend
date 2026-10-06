from app.core.bounds_calibration import compute_all_bounds, extract_latest_values
from app.data.cache.cache import get_tickers_cached, set_bounds_cached, cache_metrics


def refresh_sp500_cache(metric_fetcher, ticker_client, limit: int | None = None) -> dict:
    """Fetch all S&P 500 metrics, store them in Redis, and recompute percentile bounds."""
    tickers = get_tickers_cached(ticker_client)

    # fetch_many has rate-limiting built in + skips failures
    results = metric_fetcher.fetch_many(tickers, limit)

    if not results:
        raise RuntimeError("No metrics could be fetched, bounds not updated.")

    # Cache each ticker's metrics in Redis
    for ticker, metrics in results:
        cache_metrics(ticker, metrics)

    # _ discards the ticker, we only need the metrics here
    all_metrics = []
    for _, metrics in results:
        all_metrics.append(metrics)

    extracted = extract_latest_values(all_metrics)
    bounds = compute_all_bounds(extracted)
    set_bounds_cached(bounds)

    return bounds
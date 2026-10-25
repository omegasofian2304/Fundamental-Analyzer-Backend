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

# Generated with Claude AI, entry point for running the refresh script
# run with `python -m app.scripts.refresh_sp500_cache --limit 10`
if __name__ == "__main__":
    import argparse  # built-in module for parsing command-line arguments
    from app.data.metrics.fetch_finnhub import Finnhub
    from app.data.tickers.sp500_github_client import SP500Github

    # Create a parser that reads --limit from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None,
                        help="Number of tickers to process (for testing)")

    # Parse the arguments into an object (args.limit = 10 if you passed --limit 10)
    args = parser.parse_args()

    # Run the refresh with real implementations of the abstractions
    bounds = refresh_sp500_cache(Finnhub(), SP500Github(), limit=args.limit)
    print(f"Bounds recalculated for {len(bounds)} metrics.")
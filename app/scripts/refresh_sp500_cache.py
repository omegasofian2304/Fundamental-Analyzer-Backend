import argparse
import time

from app.core.bounds_calibration import compute_all_bounds, extract_latest_values
from app.data.cache import fetch_metric_cached, get_tickers_cached, set_bounds_cached
from app.data.metrics.fundamental_metrics_fetcher import MetricFetchError

# Finnhub allows 60 calls/minute: pause after every 55 to stay under it.
CALLS_BEFORE_PAUSE = 55
PAUSE_SECONDS = 60


def refresh_sp500_cache(limit: int | None = None) -> dict:

    tickers = get_tickers_cached(
        
    )
    if limit:
        tickers = tickers[:limit]

    all_metrics = []
    failed = []

    for i, ticker in enumerate(tickers):
        try:
            # force_refresh=True: skip the cache read, always call Finnhub
            # and overwrite the stored value.
            all_metrics.append(fetch_metric_cached(ticker, force_refresh=True))
        except MetricFetchError as exc:
            print(f"Skipping {ticker}: {exc}")
            failed.append(ticker)

        print(f"[{i + 1}/{len(tickers)}] {ticker}")

        # Failed calls also count toward Finnhub's limit, no pause after the last ticker, there is nothing left to wait for.
        if (i + 1) % CALLS_BEFORE_PAUSE == 0 and i + 1 < len(tickers):
            print(f"Rate limit: pausing {PAUSE_SECONDS}s...")
            time.sleep(PAUSE_SECONDS)

    if not all_metrics:
        raise RuntimeError("No metrics could be fetched, bounds not updated.")

    extracted = extract_latest_values(all_metrics)
    bounds = compute_all_bounds(extracted)
    set_bounds_cached(bounds)

    print(f"\nDone: {len(all_metrics)} companies cached, {len(failed)} skipped.")
    if failed:
        print(f"Skipped tickers: {', '.join(failed)}")
    print(f"Bounds stored: {bounds}")

    return bounds


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Refresh the S&P 500 Redis cache.")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="only process the first N tickers (for testing)",
    )
    args = parser.parse_args()

    refresh_sp500_cache(limit=args.limit)
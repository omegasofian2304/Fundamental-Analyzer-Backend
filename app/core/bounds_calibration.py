from app.data.metrics.fetch_finnhub import Finnhub
from app.data.metrics.fundamental_metrics_fetcher import MetricFetchError
from app.data.tickers.sp500_github_client import SP500Github
import time
import numpy as np

def get_latest_value(series):
    """
    Extract the most recent (date, value) pair from a metric's
    quarterly history, regardless of the order the API returned it in.
    """
    if not series:
        return None
    # key=... tells max() to compare only the date part of each tuple
    latest = max(series, key=lambda point: point[0])
    return latest[1]


def get_all_sp500_metrics(tickers, limit=None):
    # limit lets you test on a small subset during dev instead of
    # waiting 9 min for all 500 tickers every time.
    if limit:
        tickers = tickers[:limit]

    sp500_metrics = []
    client = Finnhub()

    # enumerate give the position and the ticker
    for i, ticker in enumerate(tickers):
        try:
            sp500_metrics.append(client.fetch_metric(ticker))
        except MetricFetchError as exc:
            print(f"Skipping {ticker}: {exc}")
            continue

        # +1 because enumerate starts at 0 this triggers after every
        # 55th call, staying safely under Finnhub's 60 calls/minute limit
        if (i + 1) % 55 == 0:
            time.sleep(60)

    return sp500_metrics


def extract_latest_values(sp500_metrics):
    """
    Transform per-company metric histories into flat lists of latest
    values per metric, ready for percentile calculation.
    """
    metric_names = ["peTTM", "netDebtToTotalEquity", "netMargin", "salesPerShare"]

    result = {"peTTM": [], "netDebtToTotalEquity": [], "netMargin": [], "salesPerShare": [],}

    for company in sp500_metrics:
        for metric_name in metric_names:
            if metric_name in company:
                series = company[metric_name]
            else:
                continue

            if not series:
                continue

            latest_value = get_latest_value(series)
            result[metric_name].append(latest_value)

    return result


def compute_percentile_bounds(metric_values, low_pct=5, high_pct=95):
    """
    Compute low, high bounds for one metric's list of values.
    """
    low_bound = np.percentile(metric_values, low_pct)
    high_bound = np.percentile(metric_values, high_pct)
    return [np.round(low_bound, 2), np.round(high_bound, 2)]


def compute_all_bounds(extracted_metrics, low_pct=5, high_pct=95):
    """
    Apply compute_percentile_bounds to every metric in the dict
    returned by extract_latest_values.
    """
    bounds = {}
    for metric in extracted_metrics:
        bounds[metric]= compute_percentile_bounds(extracted_metrics[metric], low_pct, high_pct)

    return bounds

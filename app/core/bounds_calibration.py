import numpy as np
from app.core.metric_constants import RAW_METRIC_NAMES, GROWTH_METRIC_NAME, SCORE_METRIC_NAMES

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


def get_two_values(series, offset=4):
    if not series or len(series) < offset + 1:
        return None
    sorted_series = sorted(series, key=lambda point: point[0], reverse=True)
    return sorted_series[0][1], sorted_series[offset][1]


def extract_latest_values(sp500_metrics):
    """
    Transform per-company metric histories into flat lists of latest
    values per metric, ready for percentile calculation.
    """

    result = {name: [] for name in SCORE_METRIC_NAMES}

    for company in sp500_metrics:
        for metric_name in RAW_METRIC_NAMES:
            if metric_name in company:
                series = company[metric_name]
            else:
                continue

            if not series:
                continue

            if metric_name == "salesPerShare":
                latest_value = compute_growth(series)
                if latest_value is not None:
                    result[GROWTH_METRIC_NAME].append(latest_value)
                continue

            latest_value = get_latest_value(series)

            if latest_value is None:
                continue

            result[metric_name].append(latest_value)

    return result


def compute_growth(series):
    values = get_two_values(series)
    if values is None:
        return None
    recent, previous = values
    if previous == 0:
        return None
    return (recent - previous) / previous


def compute_percentile_bounds(metric_values, low_pct=5, high_pct=95):
    """
    Compute low, high bounds for one metric's list of values.
    """
    if not metric_values:
        return None

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
        result = compute_percentile_bounds(extracted_metrics[metric], low_pct, high_pct)
        if result is not None:
            bounds[metric] = result

    return bounds


def compute_bounds(ticker_source, metric_client, limit=None):
    tickers = ticker_source.get_tickers()
    sp500_metrics = metric_client.fetch_many(tickers, limit)

    extracted = extract_latest_values(sp500_metrics)
    bounds = compute_all_bounds(extracted)

    return bounds
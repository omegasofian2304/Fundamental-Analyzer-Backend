from app.core.bounds_calibration import compute_growth, get_latest_value
from app.schemas.fundamental_metrics import FundamentalMetrics
from app.core.metric_constants import (RAW_METRIC_NAMES, GROWTH_METRIC_NAME, SCORE_METRIC_NAMES, INVERTED_METRICS,
METRIC_WEIGHTS)

def build_fundamental_metrics(metrics_of_a_ticker: dict) -> FundamentalMetrics:
    return FundamentalMetrics(**metrics_of_a_ticker)

def compute_inversed_score_per_metric(value, low, high):
    """
    Scale a raw metric value to a 0-100 score, inverted so that a
    LOW raw value produces a HIGH score (e.g. for peTTM or
    netDebtToTotalEquity, where lower is better).
    """

    if value < low:
        return 100
    elif value > high:
        return 0

    score = 100*(low - value) / (low - high)

    return 100-score


def compute_score_per_metric(value, low, high):
    """
    Scale a raw metric value to a 0-100 score
    """

    if value < low:
        return 0
    elif value > high:
        return 100

    score = 100*(low - value) / (low - high)

    return score

def prepare_ticker_to_be_computed(ticker, metric_client):
    metrics_of_a_ticker = metric_client.fetch_metric(ticker)

    result = {name: 0 for name in SCORE_METRIC_NAMES}

    for metric in RAW_METRIC_NAMES:
        if metric == "salesPerShare":
            result[GROWTH_METRIC_NAME] = compute_growth(metrics_of_a_ticker[metric])
        else:
            result[metric] = get_latest_value(metrics_of_a_ticker[metric])

    return build_fundamental_metrics(result)


def score_ticker(ticker, metric_client, bounds):

    # Pydantic model to dict, so we can index it by metric name
    metrics_of_a_ticker = prepare_ticker_to_be_computed(ticker, metric_client).model_dump()

    scores = {name: 0 for name in SCORE_METRIC_NAMES}

    for metric in SCORE_METRIC_NAMES:
        if metric in INVERTED_METRICS:
            scores[metric] = compute_inversed_score_per_metric(metrics_of_a_ticker[metric], bounds[metric][0], bounds[metric][1])
        else:
            scores[metric] = compute_score_per_metric(metrics_of_a_ticker[metric], bounds[metric][0], bounds[metric][1])

    return scores


def compute_final_score(ticker, metric_client, bounds):
    """
    Compute the weighted composite score from a list of per-metric
    scores and their corresponding weights (same order, same length).
    """

    scores = score_ticker(ticker, metric_client, bounds)

    individual_score_with_weight = []

    for metric in METRIC_WEIGHTS:
        individual_score_with_weight.append(METRIC_WEIGHTS[metric] * scores[metric])

    score = sum(individual_score_with_weight)
    return score


def compute_label(score):
    """
    Convert a composite score (0-100) into a valuation label.
    """
    if score >= 70:
        return "sous-évaluée"
    elif score <= 30:
        return "sur-évaluée"
    else:
        return "correctement valorisée"

"""
Central definitions for the 4 fundamental metrics
"""

# Field names as returned by the metrics fetcher (Finnhub), before any transformation
RAW_METRIC_NAMES = ["peTTM", "netDebtToTotalEquity", "netMargin", "salesPerShare"]

# Name used once salesPerShare has been converted into a YoY growth rate.
GROWTH_METRIC_NAME = "salesGrowth"

# Field names used everywhere downstream of the raw fetch: bounds
# dict keys, per-ticker score dict keys, weight dict keys.
SCORE_METRIC_NAMES = ["peTTM", "netDebtToTotalEquity", "netMargin", GROWTH_METRIC_NAME]

# Metrics where a LOW raw value should produce a HIGH score
INVERTED_METRICS = {"peTTM", "netDebtToTotalEquity"}

# Composite score weights. Must sum to 1.0.
METRIC_WEIGHTS = {
    "peTTM": 0.3,
    "netDebtToTotalEquity": 0.3,
    "netMargin": 0.2,
    GROWTH_METRIC_NAME: 0.2,
}
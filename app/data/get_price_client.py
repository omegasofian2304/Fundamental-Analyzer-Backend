from app.config import TWELVEDATA_API_KEY
import requests

base_url = "https://api.twelvedata.com/time_series"

class PriceHistoryError(Exception):
    pass


def get_price_history(ticker, year=5):
    """
        Fetch price history from Twelve Data.

        Args:
            ticker (str): Stock ticker symbol, e.g. "AAPL"
            year (int): Number of years of history to retrieve

        Returns:
            list[dict]: List of dictionaries with "date" and "close" keys,
            ordered from oldest to most recent.

        Example:
            get_price_history("AAPL", 8)
    """
    if not TWELVEDATA_API_KEY:
        raise PriceHistoryError("TWELVEDATA_API_KEY not set")

    params = {
        "symbol": ticker,
        "interval": "1month",
        "outputsize": year * 12,
        "apikey": TWELVEDATA_API_KEY
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise PriceHistoryError(f"network error {exc}")

    data = response.json()

    if data.get("status") == "error":
        raise PriceHistoryError(data.get("message", "Unknown Twelve Data error"))

    values = data.get("values")
    if not values:
        raise PriceHistoryError(f"No price data returned for {ticker}")

    history = []
    for entry in reversed(values):
        history.append({
            "date": entry["datetime"],
            "close": float(entry["close"])
        })

    return history

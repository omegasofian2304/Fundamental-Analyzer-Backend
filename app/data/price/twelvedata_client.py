from app.data.price.price_fetcher import PriceFetcher, PriceHistoryError
from app.config import TWELVEDATA_API_KEY
import requests


class TwelveData(PriceFetcher):
    def __init__(self, api_key=None, base_url="https://api.twelvedata.com/time_series"):
        self.api_key = api_key or TWELVEDATA_API_KEY
        self.base_url = base_url

        if not self.api_key:
            raise PriceHistoryError("TWELVEDATA_API_KEY not set")

    def fetch_price(self, ticker, year=5):
        """
            Fetch price history from Twelve Data.

            Args:
                ticker (str): Stock ticker symbol, e.g. "AAPL"
                year (int): Number of years of history to retrieve

            Returns:
                list[dict]: List of dictionaries with "date" and "close" keys,
                ordered from oldest to most recent.

            Example:
                fetch_price("AAPL", 8)
        """

        params = {
            "symbol": ticker,
            "interval": "1month",
            "outputsize": year * 12,
            "apikey": self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
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
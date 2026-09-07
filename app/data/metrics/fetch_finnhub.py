import requests
from app.data.metrics.fundamental_metrics_fetcher import MetricFetcher, MetricFetchError
from app.config import FINNHUB_API_KEY
from datetime import datetime, timedelta

class Finnhub(MetricFetcher):
    def __init__(self, api_key=None, base_url="https://finnhub.io/api/v1/stock/metric"):
        self.api_key = api_key or FINNHUB_API_KEY
        self.base_url = base_url
    def fetch_metric(self, ticker):
        """
            fetch metrics(the net debt total equity, the net margin, the peTTM and sales per share)
            for a company

            args:
                ticker (str): Stock ticker symbol, e.g. "AAPL"

            :return:
                a dict of lists of tuples

            example:
                fetch_metric("APPL")
        """

        if not self.api_key:
            raise MetricFetchError("FINNHUB_API_KEY is missing")
        params = {
            "symbol": ticker,
            "metric": "all",
            "token": self.api_key
        }

        five_years = datetime.now() - timedelta(days=5 * 365)
        six_years = datetime.now() - timedelta(days=6 * 365)

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            raise MetricFetchError(f"network error {exc}")

        data = response.json()

        try:
            quarterly = data["series"]["quarterly"]
        except KeyError:
            raise MetricFetchError(f"Format de réponse inattendu pour {ticker}")
        result={}
        metrics = {"netDebtToTotalEquity","netMargin","peTTM","salesPerShare"}

        for metric in metrics:
            try:
                serie = quarterly[metric]
            except KeyError:
                continue

            result[metric] = []

            for point in serie:
                date = datetime.strptime(point["period"], "%Y-%m-%d")
                value = point["v"]

                if date >= six_years and metric=="salesPerShare":
                    result[metric].append((date,value))

                elif date >= five_years:
                    result[metric].append((date, value))

        return result


from app.data.tickers.tickers_fetcher import TickerSource, TickerFetchError
import pandas as pd
import requests

class SP500Github(TickerSource):
    def __init__(self, url="https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"):
        self.url = url

    def get_tickers(self):
        """
        Fetch the current S&P 500 constituent tickers.

        Returns:
            list[str]: List of ticker symbols, e.g. ["AAPL", "MSFT", ...]

        Raises:
            TickerFetchError: If the data cannot be retrieved or parsed.

        Example:
            SP500GithubClient().get_tickers()
        """
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            raise TickerFetchError(f"network error {exc}")

        try:
            # response.text is raw text, not a file: StringIO makes it behave
            # like an in-memory file, the only format read_csv accepts.
            data_frame = pd.read_csv(pd.io.common.StringIO(response.text))
        except Exception as exc:
            raise TickerFetchError(f"failed to parse CSV: {exc}")

        if "Symbol" not in data_frame.columns:
            raise TickerFetchError("unexpected CSV format, 'Symbol' column missing")

        return data_frame["Symbol"].tolist()

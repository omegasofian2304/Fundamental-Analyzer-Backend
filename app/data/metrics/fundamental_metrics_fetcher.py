from abc import ABC, abstractmethod

class MetricFetcher(ABC):
    @abstractmethod
    def fetch_metric(self, ticker):
        """
        Fetch historical metric of a company

        Args:
            ticker (str): Stock ticker symbol, e.g. "AAPL"

        Returns:
            dict[liste[tuples]]:dictionnary of liste of tuples.

        Raises:
            data_finnhub_error: If the data cannot be retrieved or parsed.
        """
        pass


    def fetch_many(self, tickers, limit=None):
        """
        Fetch metrics for several tickers, skipping any that fail
        instead of aborting the whole batch.

        This default implementation has no rate limiting. Providers
        with an API call limit (like Finnhub) should override this
        method to add batching/pauses, keeping that detail out of core/.

        Args:
            tickers (list[str]): Ticker symbols to fetch.
            limit (int, optional): Cap the number of tickers fetched,
                useful for testing on a small subset instead of the
                full universe.

        Returns:
            list[dict]: One fetch_metric() result per ticker that was
            fetched successfully.
        """
        # limit lets you test on a small subset
        if limit:
            tickers = tickers[:limit]

        sp500_metrics = []

        # enumerate give the position and the ticker
        for i, ticker in enumerate(tickers):
            try:
                sp500_metrics.append(self.fetch_metric(ticker))
            except MetricFetchError as exc:
                print(f"Skipping {ticker}: {exc}")
                continue

        return sp500_metrics

class MetricFetchError(Exception):
    pass
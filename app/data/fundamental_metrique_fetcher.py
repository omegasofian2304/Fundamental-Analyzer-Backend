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

class data_metric_error(Exception):
    pass
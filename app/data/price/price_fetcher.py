from abc import ABC, abstractmethod

class PriceFetcher(ABC):
    @abstractmethod
    def fetch_price(self, ticker, year):
        """
        Fetch historical closing price data for a given ticker.

        This is the contract that any price data provider must implement.
        The chosen data source (Twelve Data, or any future provider) is
        irrelevant to the caller, only this interface matters.

        Args:
            ticker (str): Stock ticker symbol, e.g. "AAPL"
            year (int): Number of years of history to retrieve. Defaults to 5.

        Returns:
            list[dict]: List of dictionaries with "date" and "close" keys,
            ordered from oldest to most recent.

        Raises:
            PriceHistoryError: If the data cannot be retrieved or parsed.
        """
        pass

class PriceHistoryError(Exception):
    pass
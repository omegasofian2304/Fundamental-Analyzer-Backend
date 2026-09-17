from abc import ABC, abstractmethod

class TickerSource(ABC):
    @abstractmethod
    def get_tickers(self):
        """
        Fetch the list of ticker symbols for the target universe.

        Returns:
            list[str]: List of ticker symbols, e.g. ["AAPL", "MSFT", ...]

        Raises:
            TickerFetchError: If the data cannot be retrieved or parsed.
        """
        pass

class TickerFetchError(Exception):
    pass
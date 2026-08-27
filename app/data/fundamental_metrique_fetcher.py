from abc import ABC, abstractmethod

class MetriqueFetcher(ABC):
    @abstractmethod
    def fetch_metrique(self, ticker):
        """
        Fetch historical metrique of a company

        Args:
            ticker (str): Stock ticker symbol, e.g. "AAPL"

        Returns:
            dict[liste[tuples]]:dictionnary of liste of tuples.

        Raises:
            data_finnhub_error: If the data cannot be retrieved or parsed.
        """
        pass

class data_metrique_error(Exception):
    pass
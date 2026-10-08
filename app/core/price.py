from app.data.cache.cache import get_price_history_cached

def get_price_history(ticker: str, price_fetcher) -> dict:
    """Fetch cached price history for a ticker."""
    prices = get_price_history_cached(price_fetcher, ticker)
    return {
        "ticker": ticker,
        "prices": prices
    }
from app.data.score_history.history import read_score_history

def get_history(ticker: str) -> dict:
    """Fetch score history for a ticker from MySQL."""
    scores = read_score_history(ticker)
    history = [
        {"date": row.calculated_date, "score": row.score, "label": row.label}
        for row in scores
    ]
    return {"ticker": ticker, "history": history}
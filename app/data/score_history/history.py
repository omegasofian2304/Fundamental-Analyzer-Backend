from datetime import date

from sqlalchemy.orm import Session
from app.data.database import engine
from app.data.models.score_history import ScoreHistory

def read_score_history(ticker: str) -> list[ScoreHistory]:
    """Read all score history rows for a ticker, sorted by date."""
    with Session(engine) as session:
        return (
            session.query(ScoreHistory)
            .filter(ScoreHistory.company_ticker == ticker)
            .order_by(ScoreHistory.calculated_date)
            .all()
        )


def save_score_history(ticker: str, score: float, label: str, calculated_date: date) -> None:
    """Insert a new score history row"""
    with Session(engine) as session:
        entry = ScoreHistory(
            company_ticker=ticker,
            score=score,
            label=label,
            calculated_date=calculated_date,
        )
        session.add(entry)
        session.commit()
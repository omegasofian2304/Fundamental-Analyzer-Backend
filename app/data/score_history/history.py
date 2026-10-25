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
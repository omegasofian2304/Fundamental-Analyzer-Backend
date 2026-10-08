from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from app.data.database import Base

class ScoreHistory(Base):
    __tablename__ = "score_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    calculated_date = Column(Date, nullable=False)
    score = Column(Float, nullable=False)
    label = Column(String(20), nullable=False)
    company_ticker = Column(String(10), ForeignKey("company.ticker"), nullable=False)
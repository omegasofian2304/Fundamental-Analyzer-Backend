from pydantic import BaseModel
from datetime import date

class ScoreResponse(BaseModel):
    ticker: str
    score: float
    valuation_score: float
    debt_score: float
    growth_score: float
    margin_score: float
    label: str
    date: date
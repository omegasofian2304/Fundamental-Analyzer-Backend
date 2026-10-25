from pydantic import BaseModel
from datetime import date

class ScoreResponse(BaseModel):
    ticker: str
    score: float
    label: str
    date: date
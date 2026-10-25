from pydantic import BaseModel
from datetime import date

class HistoryEntry(BaseModel):
    date: date
    score: float
    label: str

class HistoryResponse(BaseModel):
    ticker: str
    history: list[HistoryEntry]
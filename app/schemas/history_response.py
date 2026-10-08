from pydantic import BaseModel

class HistoryResponse(BaseModel):
    ticker: str
    history: list[dict]
from pydantic import BaseModel

class PriceEntry(BaseModel):
    date: str
    close: float

class PriceResponse(BaseModel):
    ticker: str
    prices: list[PriceEntry]
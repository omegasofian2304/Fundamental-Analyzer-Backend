from pydantic import BaseModel

class PriceResponse(BaseModel):
    ticker: str
    prices: list[dict]
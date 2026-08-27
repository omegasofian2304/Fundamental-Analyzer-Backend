from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class FundamentalMetrics(BaseModel):
    pe_ratio: float
    debt_to_equity: float = Field(ge=0)
    revenue_growth: float
    profit_margin: float
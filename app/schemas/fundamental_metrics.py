from pydantic import BaseModel

class FundamentalMetrics(BaseModel):
    peTTM: float
    netDebtToTotalEquity: float
    salesGrowth: float
    netMargin: float
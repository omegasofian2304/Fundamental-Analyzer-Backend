from fastapi import APIRouter
from app.core.score_history import get_history
from app.schemas.history_response import HistoryResponse

router = APIRouter()

@router.get("/history/{ticker}", response_model=HistoryResponse)
def history(ticker: str):
    return get_history(ticker.upper())
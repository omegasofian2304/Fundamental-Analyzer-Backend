from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.data.models.company import read_all_companies
from app.data.database import get_db
from app.schemas.company import Company

router = APIRouter()


@router.get("/companies", response_model=list[Company])
def list_companies(db: Session = Depends(get_db)):
    return read_all_companies(db)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.data.company import read_all_companies
from app.data.database import get_db
from app.schemas.company import Company

router = APIRouter()


@router.get("/companies", response_model=list[Company])
def list_companies(db: Session = Depends(get_db)):
    try:
        return read_all_companies(db)
    except SQLAlchemyError:

        #if there is an error with SQLAlchemy raise an exception code with status 503
        raise HTTPException(status_code=503, detail="Database unavailable")
from sqlalchemy.orm import Session

from app.data.models.company import read_all_companies


def get_all_companies(db: Session):
    return read_all_companies(db)
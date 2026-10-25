from sqlalchemy import Column, String
from app.data.database import Base
from sqlalchemy.orm import Session


class Company(Base):
    __tablename__ = "company"

    ticker = Column(String(10), primary_key=True)
    name = Column(String(100), nullable=True)
    exchange = Column(String(50), nullable=True)


def read_all_companies(db: Session) -> list[Company]:
    return db.query(Company).all()


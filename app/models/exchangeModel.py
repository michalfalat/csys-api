from app.models import Base
from sqlalchemy import Column, Integer, String, Float, DateTime

class Exchange(Base):
    __tablename__ = "exchanges"

    id = Column(Integer, primary_key = True)
    created_at = Column(DateTime)
    name = Column(String(50))
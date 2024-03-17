from config.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime

class PriceDiff(Base):
    __tablename__ = "price_diffs"

    id = Column(Integer, primary_key = True)
    created_at = Column(DateTime)
    exchange_1 = Column(String(50))
    exchange_2 = Column(String(50))
    exchange_1_date = Column(DateTime)
    exchange_2_date = Column(DateTime)
    exchange_1_price = Column(Float)
    exchange_2_price = Column(Float)
    exchange_1_symbol = Column(String(50))
    exchange_2_symbol = Column(String(50))
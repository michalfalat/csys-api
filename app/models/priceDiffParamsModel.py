from app.config.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON

class PriceDiffParams(Base):
    __tablename__ = "price_diff_params"

    id = Column(Integer, primary_key = True)
    created_at = Column(DateTime)
    exchanges = Column(JSON, nullable=False, default=[])
    watched_symbols = Column(JSON, nullable=False, default=[])
    price_diff_threshold = Column(Float)
    time_diff_threshold = Column(Float)

    
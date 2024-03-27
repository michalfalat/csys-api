from app.models import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ARRAY
import datetime

class PriceDiffParams(Base):
    __tablename__ = "price_diff_params"

    id = Column(Integer, primary_key = True)
    name = Column(String(50))
    description = Column(String(200))
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    exchanges = Column(ARRAY(String), nullable=False, default=[])
    watched_symbols = Column(ARRAY(String), nullable=False, default=[])
    price_diff_threshold = Column(Float, default=0.0)
    time_diff_threshold = Column(Float, default=0.0)

    
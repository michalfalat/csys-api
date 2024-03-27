from app.models import Base
import enum
import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import ENUM

class PriceDiffType(enum.Enum):
    none = 'none'
    bid = 'bid'
    ask = 'ask'

class PriceDiff(Base):
    __tablename__ = "price_diffs"

    id = Column(Integer, primary_key = True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    exchange_1 = Column(String(50), nullable=False)
    exchange_2 = Column(String(50), nullable=False)
    exchange_1_date = Column(DateTime, nullable=False)
    exchange_2_date = Column(DateTime, nullable=False)
    exchange_1_price = Column(Float, nullable=False)
    exchange_2_price = Column(Float, nullable=False)
    exchange_1_symbol = Column(String(50), nullable=False)
    exchange_2_symbol = Column(String(50), nullable=False)
    price_diff = Column(Float)
    type = Column(ENUM(PriceDiffType, name='price_diff_type', create_type=False), default=PriceDiffType.none)
    time_diff = Column(Float)
    price_diff_params_id = Column(Integer, ForeignKey('price_diff_params.id'), nullable=True)
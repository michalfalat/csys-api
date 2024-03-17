from pydantic import BaseModel, Field
from typing import Optional, List


class PriceDiffSchema(BaseModel):
    id: int
    date: str
    exchange_1: str
    exchange_2: str
    exchange_1_date: str
    exchange_2_date: str
    exchange_1_price: float
    exchange_2_price: float
    exchange_1_symbol: str
    exchange_2_symbol: str
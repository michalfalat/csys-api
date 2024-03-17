from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi import FastAPI, Depends, Body, Query


class PriceDiffParamsSchema(BaseModel):
    id: int
    created_at: str
    exchanges: List[str]
    watched_symbols: List[str]
    price_diff_threshold: float
    time_diff_threshold: int

class PriceDiffParamsCreateSchema(BaseModel):
    exchanges: List[str] = Field(Body(...))
    watched_symbols: List[str]= Field(Body(...))
    price_diff_threshold: float= Field(Body(...))
    time_diff_threshold: int= Field(Body(...))
from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import Optional, List
from config.database import Session
from models.priceDiffModel import PriceDiff as PriceDiffModel
from fastapi.encoders import jsonable_encoder
from services.priceDiffService import PriceDiffService
from schemas.priceDiffSchema import PriceDiffSchema

price_diff_router = APIRouter()

# Get records from the price_diffs table
@price_diff_router.get('/price-diffs', tags=['price_diffs'], response_model=List[PriceDiffSchema], status_code=200)
def get_price_diffs() -> List[PriceDiffSchema]:
    db = Session()
    result = PriceDiffService(db).get_price_diffs()
    if not result:
        return JSONResponse(status_code=404, content={'message': "Not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
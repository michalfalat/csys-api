from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import Optional, List
from app.config.database import Session
from app.models.priceDiffModel import PriceDiff as PriceDiffModel
from fastapi.encoders import jsonable_encoder
from app.services.priceDiffService import PriceDiffService
from app.schemas.priceDiffSchema import PriceDiffSchema

price_diff_router = APIRouter()

# Get records from the price_diffs table
@price_diff_router.get('/', response_model=List[PriceDiffSchema], status_code=200)
def get_price_diffs() -> List[PriceDiffSchema]:
    db = Session()
    result = PriceDiffService(db).get_price_diffs()
    if not result:
        return JSONResponse(status_code=404, content={'message': "Not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# Get current differences
@price_diff_router.get('/current-differences', status_code=200)
def get_current_differences():
    db = Session()
    result = PriceDiffService(db).get_current_differences()
    if not result:
        return JSONResponse(status_code=404, content={'message': "Not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# Get strong differences
@price_diff_router.get('/strong-differences', status_code=200)
def get_strong_differences():
    db = Session()
    result = PriceDiffService(db).get_strong_differences()
    if not result:
        return JSONResponse(status_code=404, content={'message': "Not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
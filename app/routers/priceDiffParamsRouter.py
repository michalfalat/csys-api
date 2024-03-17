from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import Optional, List
from app.config.database import Session
from app.models.priceDiffModel import PriceDiff as PriceDiffModel
from fastapi.encoders import jsonable_encoder
from app.services.priceDiffParamsService import PriceDiffParamsService
from app.schemas.priceDiffParamsSchema import PriceDiffParamsSchema, PriceDiffParamsCreateSchema

price_diff_params_router = APIRouter()

# Get records from the price_diff_params table
@price_diff_params_router.get('/price-diff-params', tags=['price_diff_params'], response_model=List[PriceDiffParamsSchema], status_code=200)
def get_price_diff_params() -> List[PriceDiffParamsSchema]:
    db = Session()
    result = PriceDiffParamsService(db).get_price_diff_params()
    if not result:
        return JSONResponse(status_code=404, content={'message': "Not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# Add new record to the price_diff_params table
@price_diff_params_router.post('/price-diff-params', tags=['price_diff_params'], response_model=PriceDiffParamsSchema, status_code=201)
def add_price_diff_param(price_diff_param: PriceDiffParamsCreateSchema = Depends()) -> PriceDiffParamsSchema:
    db = Session()
    result = PriceDiffParamsService(db).add_price_diff_param(price_diff_param)
    return JSONResponse(status_code=201, content=jsonable_encoder(result))

# Get last record from the price_diff_params table
@price_diff_params_router.get('/price-diff-params/last', tags=['price_diff_params'], response_model=PriceDiffParamsSchema, status_code=200)
def get_last_price_diff_params() -> PriceDiffParamsSchema:
    db = Session()
    result = PriceDiffParamsService(db).get_last_price_diff_params()
    if not result:
        return JSONResponse(status_code=404, content={'message': "Not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
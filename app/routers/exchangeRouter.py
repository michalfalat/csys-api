from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from app.config.database import Session
from app.models.priceDiffModel import PriceDiff as PriceDiffModel
from fastapi.encoders import jsonable_encoder
from app.services.exchangeService import ExchangeService

exchange_router = APIRouter()

# Get records from the exchanges table (not currently in DB)
@exchange_router.get('/exchanges', tags=['exchanges'], response_model=List[str], status_code=200)
def get_exchanges() -> List[str]:
    db = Session()
    result = ExchangeService(db).get_exchanges()
    if not result:
        return JSONResponse(status_code=404, content={'message': "Not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@exchange_router.post('/exchanges/refresh-all', tags=['exchanges'], response_model=List[str], status_code=200)
def refresh_exchanges() -> List[str]:
    db = Session()
    result = ExchangeService(db).refresh_all_exchanges()
    if not result:
        return JSONResponse(status_code=404, content={'message': "Not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
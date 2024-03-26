import os
import asyncio
from app.config.database import Session, engine, Base
from fastapi import FastAPI
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# routers
from app.routers.priceDiffRouter import price_diff_router
from app.routers.exchangeRouter import exchange_router
from app.routers.priceDiffParamsRouter import price_diff_params_router

# services
from app.services.priceDiffService import PriceDiffService
from app.services.backgroundRunner import BackgroundRunner

# app
app = FastAPI(docs_url="/api-doc", redoc_url=None)
app.title = "CSYS API"
app.version = "0.0.1"

Base.metadata.create_all(engine)

# add routers
app.include_router(price_diff_router, prefix="/api/price-diffs", tags=['Price Diffs'])
app.include_router(exchange_router, prefix="/api/exchanges", tags=['Exchanges'])
app.include_router(price_diff_params_router)

runner = BackgroundRunner()

@app.on_event('startup')
async def app_startup():    
    db = Session()
    result = PriceDiffService(db).run_main_check_task()
    runner.task = asyncio.create_task(result)

@app.get("/stats")
def root_info():
    env_version = os.environ['VERSION']
    return 'C-SYS API 0.20 is running: Env: ' + env_version

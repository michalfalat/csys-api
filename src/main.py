import os
from config.database import Session, engine, Base
from fastapi import FastAPI
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# routers
from routers.priceDiffRouter import price_diff_router
from routers.exchangeRouter import exchange_router
from routers.priceDiffParamsRouter import price_diff_params_router

# app
app = FastAPI()
app.title = "CSYS API"
app.version = "0.0.1"

Base.metadata.create_all(engine)

# add routers
app.include_router(price_diff_router)
app.include_router(exchange_router)
app.include_router(price_diff_params_router)

# runner = BackgroundRunner()
# priceDiffCheck = PriceDiffCheck()

# @app.on_event('startup')
# async def app_startup():
#     runner.task = asyncio.create_task(priceDiffCheck.run_main(exchangeService))

@app.get("/")
def root_info():
    env_version = os.environ['VERSION']
    return 'C-SYS API 0.13 is running: Env: ' + env_version

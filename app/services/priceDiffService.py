import datetime
import asyncio
import ccxt.pro
from app.models.priceDiffModel import PriceDiff as PriceDiffModel

from concurrent.futures import ProcessPoolExecutor

differences = {}

class PriceDiffService:
    def __init__(self, db) -> None:
        self.start = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.db = db

    def get_price_diffs(self):
        result = self.db.query(PriceDiffModel).all()
        return result
    
    def get_current_differences(self):
        return differences

    async def log(self, exchange, symbol, timer=0.01):        
        while True:
            ticker = await exchange.watch_ticker(symbol)
            current_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
            ask = ticker['ask']
            bid = ticker['bid']
            value_obj = {
                'exchange': exchange.id,
                'symbol': symbol,
                'ask': ask,
                'bid': bid,
                'time': current_time
            }
            differences[str(exchange.id)] = value_obj
            #print(str(differences))
            await asyncio.sleep(timer)

    async def run_main_check_task(self):
        print('Starting main check task...')
        binanceExchange = ccxt.pro.binance()
        krakenExchange = ccxt.pro.kraken()
        binanceHasTicker = binanceExchange.has['watchTicker']
        krakenHasTicker = krakenExchange.has['watchTicker']
        print('binance has watch_ticker: ', str(binanceHasTicker))
        print('krakenExchange has watch_ticker: ', str(krakenHasTicker))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(
            self.log(binanceExchange, 'BTC/USDT'),
            self.log(krakenExchange, 'BTC/USDT'),
        ))
import datetime
import asyncio
import ccxt.pro
from app.models.priceDiffModel import PriceDiff as PriceDiffModel

from concurrent.futures import ProcessPoolExecutor

class PriceDiffService:
    def __init__(self, db) -> None:
        self.start = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.db = db

    def get_price_diffs(self):
        result = self.db.query(PriceDiffModel).all()
        return result

    async def log(self, exchange, symbol, timer=0.001):        
        while True:
            ticker = await exchange.watch_ticker(symbol)
            bid = (ticker['bid'] + ticker['ask']) / 2
            print(f'{datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")} {exchange.id}\t {symbol}: {bid}')
            await asyncio.sleep(timer)

    async def run_main(self, exchangeService):
        print('in loop before watch_ticker')
        binanceExchange = ccxt.pro.binance()
        krakenExchange = ccxt.pro.kraken()
        bitstampExchange = ccxt.pro.cryptocom()
        binanceHasTicker = binanceExchange.has['watchTicker']
        krakenHasTicker = krakenExchange.has['watchTicker']
        bitstampHasTicker = bitstampExchange.has['watchTicker']
        # symbols = binanceExchange.market_symbols()
        # print(*symbols, sep = ", ")
        print('binance has watch_ticker: ', str(binanceHasTicker))
        print('krakenExchange has watch_ticker: ', str(krakenHasTicker))
        print('bitstamp  has watch_ticker: ', str(bitstampHasTicker))
        ticker  = await bitstampExchange.watch_ticker('BTC/USDT')
        print(ticker['bid'])
        print('in loop after')

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(
            self.log(binanceExchange, 'BTC/USDT'),
            self.log(krakenExchange, 'BTC/USDT'),
            self.log(bitstampExchange, 'BTC/USDT'),
        ))
        print('in loop')
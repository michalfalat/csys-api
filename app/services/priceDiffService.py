import datetime
import asyncio
import ccxt.pro
from app.models.priceDiffModel import PriceDiff as PriceDiffModel

from concurrent.futures import ProcessPoolExecutor

differences = {}
strongDifferencesList = []

class PriceDiffService:
    def __init__(self, db) -> None:
        self.start = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.db = db

    def get_price_diff_percentage(self, number1, number2) -> bool:
        if number1 == 0 or number2 == 0:
            return False
        diff = abs(number1 - number2)
        percentage = (diff / number1) * 100
        return percentage

    def get_price_diffs(self):
        result = self.db.query(PriceDiffModel).all()
        return result
    
    def get_current_differences(self):
        return differences
    
    def get_strong_differences(self):
        return strongDifferencesList
    
    async def check_differences(self, timer=0.01):
        while True:
            try:
                diff_perccent_threshold = 0.2 # 0.2%
                # iterate over differences and check if there is a big difference  between the exchanges
                for key in differences.keys():
                    for key2 in differences.keys():
                        if key != key2:
                            ask1 = differences[key]['ask']
                            ask2 = differences[key2]['ask']
                            bid1 = differences[key]['bid']
                            bid2 = differences[key2]['bid']
                            ask_diff = self.get_price_diff_percentage(ask1, ask2)
                            bid_diff = self.get_price_diff_percentage(bid1, bid2)
                            if ask_diff > diff_perccent_threshold or bid_diff > diff_perccent_threshold:
                                print('Found a big difference between exchanges: ', str(key), str(key2))
                                print('ask_diff: ', str(ask_diff))
                                print('bid_diff: ', str(bid_diff))
                                value_obj = {
                                    'exchange1': key,
                                    'exchange2': key2,
                                    'ask_diff': ask_diff,
                                    'bid_diff': bid_diff,
                                    'ask_price1': ask1,
                                    'ask_price2': ask2,
                                    'bid_price1': bid1,
                                    'bid_price2': bid2,
                                    'time': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
                                }
                                strongDifferencesList.append(value_obj)
              
            except Exception as e:
                print('PriceDiffService check_differences Error: ', str(e))
            #print(str(differences))
            await asyncio.sleep(timer)

    async def log(self, exchange, symbol, timer=0.01):        
        while True:
            try:
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
            except Exception as e:
                print('PriceDiffService log Error: ', symbol, str(exchange), str(e))
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
            self.check_differences(0.05)
        ))
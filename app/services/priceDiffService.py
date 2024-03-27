import datetime
import asyncio
import ccxt.pro
from app.models.priceDiffModel import PriceDiff as PriceDiffModel
from app.models.priceDiffModel import PriceDiffType

from concurrent.futures import ProcessPoolExecutor

differences = {}

class PriceDiffService:
    def __init__(self, db) -> None:
        self.start = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.db = db

    def get_price_diff_percentage(self, number1, number2) -> float:
        if number1 == 0 or number2 == 0:
            return 0
        diff = abs(number1 - number2)
        percentage = (diff / number1) * 100
        return percentage

    def get_price_diffs(self):
        result = self.db.query(PriceDiffModel).all()
        return result
    
    def add_price_diff(self, price_diff):
        self.db.add(price_diff)
        self.db.commit()
        self.db.refresh(price_diff)
        return price_diff
    
    def get_current_differences(self):
        return differences
    
    def get_significant_differences(self):
        return self.db.query(PriceDiffModel).all()
    
    async def check_differences(self, timer=0.01):
        while True:
            try:
                diff_percent_threshold = 0.1 # 0.1%
                # iterate over differences and check if there is a big difference  between the exchanges
                for exchange_1 in differences.keys():
                    for exchange_2 in differences.keys():
                        if exchange_1 != exchange_2:
                            exchange_1_ask = differences[exchange_1]['ask']
                            exchange_2_ask = differences[exchange_2]['ask']
                            exchange_1_bid = differences[exchange_1]['bid']
                            exchange_2_bid = differences[exchange_2]['bid']
                            exchange_1_date = differences[exchange_1]['date']
                            exchange_2_date = differences[exchange_2]['date']
                            exchange_1_symbol = differences[exchange_1]['symbol']
                            exchange_2_symbol = differences[exchange_2]['symbol']
                            ask_diff = self.get_price_diff_percentage(exchange_1_ask, exchange_2_ask)
                            bid_diff = self.get_price_diff_percentage(exchange_1_bid, exchange_2_bid)
                            time_diff = abs(exchange_1_date - exchange_2_date).total_seconds()
                            if ask_diff > diff_percent_threshold:
                                # print('Found a significant ask price difference between exchanges: ', str(exchange_1), str(exchange_2), str(ask_diff))
                                priceDiffModel = PriceDiffModel()
                                priceDiffModel.created_at = datetime.datetime.now(tz=datetime.timezone.utc)
                                priceDiffModel.exchange_1 = exchange_1
                                priceDiffModel.exchange_2 = exchange_2
                                priceDiffModel.exchange_1_date = exchange_1_date
                                priceDiffModel.exchange_2_date = exchange_2_date
                                priceDiffModel.exchange_1_price = exchange_1_ask
                                priceDiffModel.exchange_2_price = exchange_2_ask
                                priceDiffModel.exchange_1_symbol = exchange_1_symbol
                                priceDiffModel.exchange_2_symbol = exchange_2_symbol
                                priceDiffModel.price_diff = ask_diff
                                priceDiffModel.type = PriceDiffType.ask
                                priceDiffModel.time_diff = time_diff
                                priceDiffModel.price_diff_params_id = None

                                self.add_price_diff(priceDiffModel)
                                await asyncio.sleep(0.1)

                            if bid_diff > diff_percent_threshold:
                                # print('Found a significant bid price difference between exchanges: ', str(exchange_1), str(exchange_2), str(bid_diff))
                                priceDiffModel = PriceDiffModel()
                                priceDiffModel.created_at = datetime.datetime.now(tz=datetime.timezone.utc)
                                priceDiffModel.exchange_1 = exchange_1
                                priceDiffModel.exchange_2 = exchange_2
                                priceDiffModel.exchange_1_date = exchange_1_date
                                priceDiffModel.exchange_2_date = exchange_2_date
                                priceDiffModel.exchange_1_price = exchange_1_bid
                                priceDiffModel.exchange_2_price = exchange_2_bid
                                priceDiffModel.exchange_1_symbol = exchange_1_symbol
                                priceDiffModel.exchange_2_symbol = exchange_2_symbol
                                priceDiffModel.price_diff = bid_diff
                                priceDiffModel.type = PriceDiffType.bid
                                priceDiffModel.time_diff = time_diff
                                priceDiffModel.price_diff_params_id = None

                                self.add_price_diff(priceDiffModel)
                                await asyncio.sleep(0.1)
              
            except Exception as e:
                print('PriceDiffService check_differences Error: ', str(e))
            await asyncio.sleep(timer)

    async def log(self, exchange, symbol, timer=0.01):        
        while True:
            try:
                ticker = await exchange.watch_ticker(symbol)
                current_date = datetime.datetime.now(tz=datetime.timezone.utc)
                ask = ticker['ask']
                bid = ticker['bid']
                value_obj = {
                    'exchange': exchange.id,
                    'symbol': symbol,
                    'ask': ask,
                    'bid': bid,
                    'date': current_date
                }
                differences[str(exchange.id)] = value_obj
            except Exception as e:
                print('PriceDiffService log Error: ', symbol, str(exchange), str(e))
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
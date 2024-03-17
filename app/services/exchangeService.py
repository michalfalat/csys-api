import ccxt
from app.models.exchangeModel import Exchange as ExchangeModel
import datetime

class ExchangeService:
    def __init__(self, db) -> None:
        self.db = db
    
    def add_exchange(self, exchange):
        self.db.add(exchange)

    def refresh_all_exchanges(self):
        self.db.query(ExchangeModel).delete()
        for exchange in ccxt.exchanges:
            mapped_exchange = ExchangeModel()
            mapped_exchange.name = exchange
            mapped_exchange.created_at = datetime.datetime.now()
            self.add_exchange(mapped_exchange)        
        self.db.commit()
        self.db.refresh()
        return self.get_exchanges()

    def get_exchanges(self):
        return self.db.query(ExchangeModel).all() 
  
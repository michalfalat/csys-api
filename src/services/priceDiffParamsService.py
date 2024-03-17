from models.priceDiffParamsModel import PriceDiffParams as PriceDiffParamsModel
import datetime

class PriceDiffParamsService:
    def __init__(self, db) -> None:
        self.db = db

    def get_price_diff_params(self):
        result = self.db.query(PriceDiffParamsModel).all()
        return result
    
    def get_last_price_diff_params(self):
        result = self.db.query(PriceDiffParamsModel).order_by(PriceDiffParamsModel.id.desc()).first()
        return result
    
    def add_price_diff_param(self, price_diff_param):
        print('add_price_diff_param: ', price_diff_param)
        mapped_price_diff_param = PriceDiffParamsModel()
        mapped_price_diff_param.created_at = datetime.datetime.now()
        mapped_price_diff_param.exchanges = price_diff_param.exchanges
        mapped_price_diff_param.watched_symbols = price_diff_param.watched_symbols
        mapped_price_diff_param.price_diff_threshold = price_diff_param.price_diff_threshold
        self.db.add(mapped_price_diff_param)
        self.db.commit()
        return self.get_price_diff_params()
   
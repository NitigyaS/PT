from datetime import datetime
from random import random, randrange
from time import sleep

from PyTrade.feeds.Feed import Feed


class RandomFeed(Feed):
    """Generates a random feed. It inherits the Feed class."""

    def __init__(self, stock_name="STOCK", exchange_name="EXCHANGE"):
        super().__init__(stock_name, exchange_name)
        self.open = random()*100

    def generate_random_feed(self, show_time_stamp_in_milli=False, show_volume=False):
        new_close = self.random_decimal(self.open)
        data = {"open": self.open,
                "close": new_close,
                "high": self.random_decimal(self.open),
                "low": self.random_decimal(self.open)
                }

        self.open = new_close
        if show_time_stamp_in_milli:
            data["timestamp"] = datetime.timestamp(datetime.now())*10e2
        if show_volume:
            data["volume"] = randrange(10000, 20000)
        return data

    def get_live_feed(self,):
        while True:
            data = self.generate_random_feed(show_time_stamp_in_milli=True,show_volume=True)
            live_feed = {"code": 200,
                         "status": "OK",
                         "timestamp": datetime.isoformat(datetime.now()),
                         "message": "success",
                         "data": data
                        }
            yield live_feed

    def get_historical_data(self, from_start_date, to_end_date):
        length = datetime.strptime(to_end_date, '%d/%m/%Y').date() - \
                 datetime.strptime(from_start_date, '%d/%m/%Y').date()
        data = []
        for i in range(abs(length.days)):
            data.append(self.generate_random_feed(show_time_stamp_in_milli=True,show_volume=True))
        live_feed = {"code": 200,
                     "status": "OK",
                     "timestamp": datetime.isoformat(datetime.now()),
                     "message": "success",
                     "data": data
                     }
        return live_feed

    @staticmethod
    def random_decimal(number, min_variation=-2, max_variation=3):
        return number + number * randrange(min_variation, max_variation) / 100


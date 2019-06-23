import csv
import os
from collections import OrderedDict
from datetime import datetime
from time import sleep

from PyTrade.feeds.Feed import Feed


class CSVFeed(Feed):
    """Generates a feeds from file in CSV. It inherits the Feed class."""

    def __init__(self, stock_name="STOCK", exchange_name="EXCHANGE"):
        super().__init__(stock_name, exchange_name)
        self.csv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                     "resources/" +
                                     stock_name.upper() + "_" +
                                     exchange_name.upper() + ".csv")
        self.feed_data = {"code": 200,
                          "status": "OK",
                          "timestamp": datetime.isoformat(datetime.now()),
                          "message": "success",
                          "data": list()
                          }
        self.csv_reader()

    def csv_reader(self):
        """
        Method reads the CSV file in resources directory. It performs the follwoing actions
        1: Convert CSV -> OrderDict -> dict
        2: Convert dict items to there desired types
        3: Change the name of keys such as date -> timestamp
        :return:
        None
        """
        with open(self.csv_path) as csv_file:
            csv_feed = csv.DictReader(csv_file, skipinitialspace=True)
            float_values = ("open", "low", "close", "high")
            for row in csv_feed:
                row2 = dict((k, float(v)) for k, v in row.items() if k in float_values)
                row2["timestamp"] = datetime.timestamp(datetime.strptime(row["date"], '%d-%b-%Y'))
                row2["volume"] = int(row["volume"])
                self.feed_data["data"].append(row2)

    def get_live_feed(self):
        for i in range(len(self.feed_data["data"])):
            live_feed = {"code": 200,
                         "status": "OK",
                         "timestamp": datetime.isoformat(datetime.now()),
                         "message": "success",
                         "data": self.feed_data["data"][i]
                         }
            yield live_feed

    def get_historical_data(self, from_start_date=None, to_end_date=None):
        if from_start_date is None and to_end_date is None:
            start_index = 0
        else:
            length = datetime.strptime(to_end_date, '%d/%m/%Y').date() - \
                 datetime.strptime(from_start_date, '%d/%m/%Y').date()
            start_index = -abs(length.days)

        historical_feed = {"code": 200,
                           "status": "OK",
                           "timestamp": datetime.isoformat(datetime.now()),
                           "message": "success",
                           "data": self.feed_data["data"][start_index:]
                           }
        return historical_feed

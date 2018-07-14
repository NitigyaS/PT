from abc import ABC, abstractmethod


class Feed(ABC):
    """
    Feed Class to be inherited by other Feed classes.
    """
    def __init__(self,stock_name,exchange_name):
        """
        Initialization method for the class
        :param stock_name:
        :param exchange_name:
        """
        self.stock_name = stock_name
        self.exchange_name = exchange_name

    @abstractmethod
    def get_live_feed(self):
        """
        Method is a generator method and returns one feed at a time.
        :return:
        Method returns the data in following format:
        {
            "code":200,
            "status":"OK",
            "timestamp":"2017-07-19T11:11:32+05:30",
            "message":"feed",
            "data":{
                "timestamp":1454498203000,
                "exchange":"NSE_INDEX",
                "symbol":"NIFTY_100",
                "open":7482.5,
                "high":7510.4,
                "low":7441.5,
                "close":7452.05,
            }
        }
        """
        pass

    @abstractmethod
    def get_historical_data(self, from_start_date, to_end_date):
        """
        Method takes a start date and end date and returns data between those 2 dates excluding the end_date.
        :param from_start_date:
        :param to_end_date:
        :return:
        Method returns the data in following format:
        {
            "code":200,
            "status":"OK",
            "timestamp":"2017-07-19T11:11:32+05:30",
            "message":"feed",
            "data":[
            {
                "timestamp":1454498203000,
                "exchange":"NSE_INDEX",
                "symbol":"NIFTY_100",
                "open":7482.5,
                "high":7510.4,
                "low":7441.5,
                "close":7452.05,
            },
            {
                "timestamp":1454498203000,
                "exchange":"NSE_INDEX",
                "symbol":"NIFTY_100",
                "open":7482.5,
                "high":7510.4,
                "low":7441.5,
                "close":7452.05,
            }
            ]
        }
        """
        pass

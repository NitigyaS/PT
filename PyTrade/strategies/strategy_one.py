import logging
import numpy
import talib

from PyTrade.strategies.strategy import Strategy, StrategyFailedException
from conf.logging import create_logger

create_logger()


class StrategyOne(Strategy):

        def __init__(self):
            super().__init__()
            self.rsi = None
            self.parameters = {
                "rsi_lookback_period": 14,
                "rsi_overvalue_limit": 60,
                "rsi_undervalue_limit": 35
            }

        def evaluate(self,numpy_array):
            if type(numpy_array) is not numpy.ndarray:
                raise StrategyFailedException(1,"Feed Data received is not a  numpy rcarray. ")
                logging.error("Feed Data received is not a  numpy rcarray")
            self.rsi = talib.RSI(numpy_array["close"], self.parameters["rsi_lookback_period"])
            print("RSI: ", self.rsi[-1] , "ClosePrice: ",numpy_array["close"][-1] )
            rsi = self.rsi[-1]
            if rsi < self.parameters["rsi_undervalue_limit"]:
                self.set_states(enter_strategy=True)
            elif rsi > self.parameters["rsi_overvalue_limit"]:
                self.set_states(exit_strategy=True)
            else:
                self.set_states()




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

        def evaluate(self,numpy_array):
            if type(numpy_array) is not numpy.ndarray:
                raise StrategyFailedException(1,"Feed Data received is not a  numpy rcarray. ")
                logging.error("Feed Data received is not a  numpy rcarray")
            self.rsi = talib.RSI(numpy_array["close"], timeperiod=14)
            print("RSI: " , self.rsi[-1] , "ClosePrice: ",numpy_array["close"][-1] )
            rsi = self.rsi[-1]
            if rsi < 35:
                self.set_states(enter_strategy=True,exit_strategy=False)
            elif rsi > 60:
                self.set_states(enter_strategy=False,exit_strategy=True)
            else:
                self.set_states()




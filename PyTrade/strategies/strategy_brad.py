import logging
import numpy
import talib
from matplotlib import pyplot as plt

from PyTrade.strategies.strategy import Strategy, StrategyFailedException, StrategyNotReady
from conf.logging import create_logger

# Start Logger
create_logger()

class StrategyBRAD(Strategy):

    def __init__(self):
        super().__init__()
        self.numpy_array = None
        self.rsi = None
        self.bollinger_bandwidth = None
        self.dmi_difference = None
        self.bw_slope_angle = None
        self.rsi_slope_angle = None
        self.stop_loss_limit = 0
        self.parameters = {
            "rsi_lookback_period": 14,
            "bb_lookback_period": 20,
            "rsi_slope_period": 5,
            "bbw_slope_period": 5,
            "bbw_volatility_threshold": 3
        }

    @staticmethod
    def __slope_to_degrees(numpy_slope_series):
        if type(numpy_slope_series) is not numpy.ndarray:
            raise StrategyFailedException(2, "Slope to Degree Conversion : Not a numpy array ")
        return numpy.degrees(numpy.arctan(numpy_slope_series))

    @staticmethod
    def __degrees_to_slope(numpy_degree_series):
        if type(numpy_degree_series) is not numpy.ndarray:
            raise StrategyFailedException(2, "Degree to Slope Conversion : Not a numpy array ")
        return numpy.tan(numpy.radians(numpy_degree_series))

    @staticmethod
    def __stop_loss_dist_rsi(rsi):
        """
        Calculate Stop Loss Distance as a function of RSI
        Stop Loss Distance is inversely promotional to RSI
        :param rsi:
        :return: stopLossDistance
        """
        return (100 - rsi)/1000.0  # return value between 0 - 0.1

    def evaluate(self, numpy_array):
        assert isinstance(numpy_array, numpy.ndarray)
        self.numpy_array = numpy_array
        try:
            self.__calculate_indicator()
            self.__build_strategy()
        except StrategyNotReady:
            pass
            # logging.info("Skipping...")
        return None

    def __calculate_indicator(self):
        # Create RSI Series
        self.rsi = talib.RSI(self.numpy_array["close"], self.parameters["rsi_lookback_period"])

        # Create Bollinger Bands
        bollinger_upper, bollinger_middle, bollinger_lower = talib.BBANDS(self.numpy_array["close"], self.parameters["bb_lookback_period"])
        self.bollinger_bandwidth = ((bollinger_upper - bollinger_lower) / bollinger_middle)*100

        # Calculate Directional Indicators.
        minus_dmi = talib.MINUS_DI(high=self.numpy_array["high"],
                                   low=self.numpy_array["low"],
                                   close=self.numpy_array["close"])
        plus_dmi = talib.PLUS_DI(high=self.numpy_array["high"],
                                 low=self.numpy_array["low"],
                                 close=self.numpy_array["close"])

        # If Directional Indicator gives Upward Direction.
        self.dmi_difference = plus_dmi - minus_dmi

        # Slope Calculation : Throws error if value is yet NaN
        try:
            self.rsi_slope_angle = self.__slope_to_degrees(talib.LINEARREG_SLOPE(self.rsi,
                                                                                 self.parameters["rsi_slope_period"]))
            self.bw_slope_angle = self.__slope_to_degrees(talib.LINEARREG_SLOPE(self.bollinger_bandwidth,
                                                                                self.parameters["bbw_slope_period"]))
        except Exception:
            #logging.info("Value of RSI and Bollinger is null")
            raise StrategyNotReady(1, "Value of RSI and Bollinger is null")
        return None

    def __build_strategy(self):
        logging.info("START_BUILD_STRATEGY ")
        logging.info("CLOSE_PRICE, "+ str(self.numpy_array["close"][-1]))

        # Entry Rules
        volatility_condition = self.bollinger_bandwidth[-1] >= self.parameters["bbw_volatility_threshold"]    # Volatility in increasing.
        rsi_slope_condition = 6 < self.rsi_slope_angle[-1] < 89     # If RSI is moving up
        dmi__condition = self.dmi_difference[-1] > -1                # if PDMI > MDMI

        # Exit Rules
        self.stop_loss_limit = self.__stop_loss_limit()
        bbw_slope_condition = -89 < self.bw_slope_angle[-1] < 0
        stop_loss_condition = self.numpy_array["close"][-1] <= self.stop_loss_limit

        logging.info("STOP_LOSS_LIMIT, "+ str(self.stop_loss_limit))
        if volatility_condition and rsi_slope_condition and dmi__condition:
            logging.info("SIGNAL_BUY, "+ str(self.numpy_array["close"][-1]))
            self.set_states(enter_strategy=True)

        # Exit if Volatility is ending or Stop Loss Breached
        elif bbw_slope_condition or stop_loss_condition:
            logging.info("SIGNAL_SELL, "+ str(self.numpy_array["close"][-1]))
            self.set_states(exit_strategy=True)
            self.stop_loss_limit = 0
        else:
            self.set_states()
        logging.info("END_BUILD_STRATEGY")

    def __stop_loss_limit(self):
        close = self.numpy_array["close"][-1]
        stop_loss_distance = self.__stop_loss_dist_rsi(self.rsi[-1])*close
        if (close - stop_loss_distance) > self.stop_loss_limit:
            self.stop_loss_limit = close - stop_loss_distance
        return self.stop_loss_limit

    def plot_graph(self):
        plt.rc('axes', grid=True)
        plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5, alpha=1)

        textsize = 9
        left, width = 0.1, 0.8
        rect1 = [left, 0.7, width, 0.2]
        rect2 = [left, 0.3, width, 0.4]
        rect3 = [left, 0.1, width, 0.2]
        axescolor = '#f6f6f6'  # the axes background color
        fillcolor = 'red'     # the line colour

        # Calculation of Date to be shown on X-axis
        date = self.numpy_array["timestamp"]

        fig = plt.figure(facecolor='white')

        ax1 = fig.add_axes(rect1, facecolor=axescolor)  # left, bottom, width, height
        ax2 = fig.add_axes(rect2, facecolor=axescolor, sharex=ax1)
        ax3 = fig.add_axes(rect3, facecolor=axescolor, sharex=ax1)

        # Plot the relative strength indicator

        ax1.plot(date, self.rsi, color=fillcolor, lw=1)
        ax1.axhline(70, color="pink", lw=1,)
        ax1.axhline(30, color="lightgreen", lw=1,)
        ax1.text(0.6, 0.9, '>70 = overbought', va='top', transform=ax1.transAxes, fontsize=textsize)
        ax1.text(0.6, 0.1, '<30 = oversold', transform=ax1.transAxes, fontsize=textsize)
        ax1.set_ylim(0, 100)
        ax1.set_yticks([30, 70])
        ax1.text(0.025, 0.95, 'RSI (14)', va='top', transform=ax1.transAxes, fontsize=textsize)
        ax1.set_title('BRAD Graph')

        # Calculate Bollinger bands
        bollinger_upper, bollinger_middle, bollinger_lower = talib.BBANDS(self.numpy_array["close"])

        ax2.plot(date, self.numpy_array["close"], color='red', lw=1, label='Close')
        ax2.plot(date, bollinger_upper, color='black', lw=0.5, label='B_UP (21)')
        ax2.plot(date, bollinger_middle, color='blue', lw=0.5, label='B_MID (21)')
        ax2.plot(date, bollinger_lower, color='black', lw=0.5, label='B_LOW (21)')
        ax2.text(0.025, 0.95, "Bollinger Bands", va='top', transform=ax2.transAxes, fontsize=textsize)

        # Plot the Bollinger Bandwidth
        ax3.plot(date, self.bollinger_bandwidth, color=fillcolor, lw=1, label='BBW')
        ax3.text(0.025, 0.95, 'Bollinger Bandwidth', va='top',
                 transform=ax3.transAxes, fontsize=textsize)

        # Rotate and Right Align
        for ax in ax1, ax2, ax3:
            if ax != ax3:
                for label in ax.get_xticklabels():
                    label.set_visible(False)
            else:
                for label in ax.get_xticklabels():
                    label.set_rotation(30)
                    label.set_horizontalalignment('right')

        # Save the output in an Image
        fig.savefig('StrategyBRAD_plot.svg', format='svg', dpi=1200)

        # Show the Graph on Screen.
        plt.show()

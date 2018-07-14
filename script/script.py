from time import sleep

from PyTrade.feeds.CSVFeed import CSVFeed
from PyTrade.feeds.RandomFeed import RandomFeed
from PyTrade.serializer.numpyserializer import NumpySerializer
from PyTrade.strategies.strategy_brad import StrategyBRAD
from PyTrade.strategyanalyser.strategyanalyser import StrategyAnalyser

from conf.logging import create_logger

create_logger()


def loop_on_history():
    # Get Feed from CSV file
    csv_feed = CSVFeed("TCS", "NSE")
    feed = csv_feed.get_historical_data("01/07/2017", "30/09/2017")

    # Create a Serializer convert csv data to numpy
    numpy_serializer = NumpySerializer(feed["data"])
    feed_data = numpy_serializer.get_series()

    # Create Strategy
    s = StrategyBRAD()
    for i in range(1, len(feed_data)):

        # Take initial i bars from feed
        sub_feed = feed_data[:i]
        # Evaluate the strategy on current feed on length i.
        s.evaluate(sub_feed)
        print("evaluating: ", sub_feed["close"][-1])
        if s.should_enter():
            print("Entered at ,", sub_feed["close"][-1])
            pass
        elif s.should_exit():
            print("Exit at ,", sub_feed["close"][-1])
            pass
        #sleep(1)


def loop_on_live():
    csv_feed = CSVFeed("TCS", "NSE")
    numpy_serializer = NumpySerializer()
    strategy_analyser = StrategyAnalyser()
    strategy = StrategyBRAD()
    for new_feed in csv_feed.get_live_feed():
        feed_data = numpy_serializer.add_bar(new_feed["data"])
        #print(feed_data["close"])
        strategy.evaluate(feed_data)
        if strategy.should_enter():
            strategy_analyser.add_trade(bought_at=feed_data["close"][-1])
        if strategy.should_exit():
            strategy_analyser.add_trade(sold_at=feed_data["close"][-1])

    # Analyses of the Strategy
    print("\n# Analyses of the Strategy\n")
    print("Buy and Hold Amount: ", strategy_analyser.buy_hold_amount )
    print("Total Profit: ", strategy_analyser.total_profit)
    print("Number of Trades: ", strategy_analyser.total_trades)
    print("Profit per Trade: ", strategy_analyser.profit_per_trade)
    strategy_analyser.print_all_trades()


def plot_graph():
    csv_feed = CSVFeed("BIOCON", "NSE")
    feed = csv_feed.get_historical_data("01/07/2017", "15/6/2018")

    # Create a Serializer convert csv data to numpy
    numpy_serializer = NumpySerializer(feed["data"])
    feed_data = numpy_serializer.get_series()

    # Create Strategy
    s = StrategyBRAD()
    s.evaluate(feed_data)
    s.plot_graph()


if __name__ == '__main__':
    loop_on_live()

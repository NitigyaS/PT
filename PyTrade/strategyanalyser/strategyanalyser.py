import sqlite3
from matplotlib import pyplot as plt

import numpy


class StrategyAnalyser():

    def __init__(self,db_name,table_name="trades",slippage=0, brokerage_percentage=0.01 , transactional_charge=0.00325, ):
        self.buy_orders = list()
        self.sell_orders = list()
        self.db_name = "/tmp/" + db_name + ".db"
        self.slippage = slippage
        self.trades = list()
        self.transactional_cost = list()
        brokerage = brokerage_percentage/100
        transactional_charge = transactional_charge/100

        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        for price in c.execute('''select price from ''' + table_name +''' where trans="BUY"'''):
            self.buy_orders.append(price[0])

        for price in c.execute('''select price from ''' + table_name +''' where trans="SELL"'''):
            self.sell_orders.append(price[0])

        for trade_number in range(len(self.sell_orders)):
            profit_loss = self.sell_orders[trade_number] - self.buy_orders[trade_number]
            # Transactional Cost
            cost = self.sell_orders[trade_number]*brokerage + self.buy_orders[trade_number]*brokerage+(transactional_charge)
            cost += cost*0.18
            self.transactional_cost.append(cost)
            self.trades.append(profit_loss)

        conn.commit()
        conn.close()

    def analyse(self):
        # Analysis

        # Metrics Calculation

        total_trades = len( self.trades)
        gross_loss = sum(trade for trade in self.trades if trade <=0)
        gross_profit = sum(trade for trade in self.trades if trade > 0)
        net_profit = gross_profit + gross_loss
        average_trade = net_profit/total_trades
        profit_factor = gross_profit / -gross_loss
        number_profit_trades = sum(trade <= 0 for trade in self.trades)
        number_loss_trades = sum(trade > 0 for trade in self.trades)
        average_winner = gross_profit / number_profit_trades
        average_loser = gross_loss / number_loss_trades
        total_transactional_cost = sum(cost for cost in self.transactional_cost );

        ## DrawDown Calculations
        max_drawdown = 0
        drawdown = 0
        for trade in self.trades:
            if trade <= 0:
                drawdown += trade
            if trade > 0 and max_drawdown > drawdown:
                max_drawdown = drawdown
                drawdown = 0

        # Expectancy = (average $ winners * win % + average $ losers * lose %) / (−average $ losers)
        tharp_expectancy = (average_trade) / -average_loser

        analysis = dict()
        analysis["hold and wait"] = self.sell_orders[-1] - self.buy_orders[0]
        analysis["gross profit"] = gross_profit
        analysis["gross loss"] = gross_loss
        analysis["transactional cost"] = total_transactional_cost
        analysis["net profit"] = net_profit - total_transactional_cost
        analysis["profit factor"] = profit_factor
        analysis["total self.trades"] = total_trades
        analysis["winning self.trades"] = number_profit_trades
        analysis["losing self.trades"] = number_loss_trades

        analysis["profitable self.trades"]= (number_profit_trades / total_trades) * 100
        analysis["average trade"] = average_trade
        analysis["average winner"] =  average_winner
        analysis["average loser"] = average_loser
        analysis["drawdown"] = max_drawdown
        analysis["drawdown"] = max_drawdown
        analysis["profit on drawdown"] = (net_profit / -max_drawdown) * 100
        analysis["tharp expectancy"] = tharp_expectancy

        return analysis

    def plot_equity_curve(self ):

        #Create Equity cureve line
        investment_progression = list()
        investment = self.buy_orders[0]
        investment_progression.append(investment)
        for trade in self.trades:
            investment += trade
            investment_progression.append(investment)

        numpy_investment_series = numpy.array(investment_progression)
        numpy_investment_series = (numpy_investment_series/self.buy_orders[0])*100 - 100
        #
        plt.rc('axes', grid=True)
        plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5, alpha=1)
        plt.title("Equity Curve")
        plt.ylabel("Profit/Loss")
        plt.xlabel("No. of self.trades")
        plt.plot(numpy_investment_series)

        plt.axhline(0,color="red" , lw=0.5)
        plt.show()


    def monte_carlo_simulation(self,starting_equity=10000, max_trade=100):
        stop_trading_equity = starting_equity*0.60      #if Investment falls below 40%
        max_trades = 100





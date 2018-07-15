import sqlite3
from matplotlib import pyplot as plt

import numpy


class StrategyAnalyser():

    def __init__(self,db_name,slippage=0, brokerage=0):
        self.buy_orders = list()
        self.sell_orders = list()
        self.db_name = "/tmp/" + db_name + ".db"
        self.slippage = slippage
        self.brokerage = brokerage

        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        for price in c.execute('''select price from trades where trans="BUY"'''):
            self.buy_orders.append(price[0])

        for price in c.execute('''select price from trades where trans="SELL"'''):
            self.sell_orders.append(price[0])

        conn.commit()
        conn.close()

        #print(type(self.buy_price), self.buy_price)



    def analyse(self):
        ## Analysis
        loss_trades = list()
        profit_trades = list()
        gross_profit = 0;
        gross_loss = 0;

        # Metrics Calculation
        for trade_number in range(len(self.sell_orders)):
            diff = self.sell_orders[trade_number] - self.buy_orders[trade_number]
            if diff > 0:
                gross_profit += diff
                profit_trades.append((self.buy_orders[trade_number], self.sell_orders[trade_number]))
            elif diff <= 0:
                gross_loss += diff
                loss_trades.append((self.buy_orders[trade_number], self.sell_orders[trade_number]))

        net_profit = gross_profit + gross_loss
        profit_factor = gross_profit / -gross_loss
        total_trades = len(self.sell_orders)
        number_profit_trades = len(profit_trades)
        number_loss_trades = len(loss_trades)
        average_winner = gross_profit / number_profit_trades
        average_loser = gross_loss / number_loss_trades

        ## DrawDown Calculations
        max_drawdown = 0
        drawdown = 0
        for trade_number in range(len(self.sell_orders)):
            diff = self.sell_orders[trade_number] - self.buy_orders[trade_number]
            if diff <= 0:
                drawdown += diff
            if diff > 0 and max_drawdown > drawdown:
                max_drawdown = drawdown
                drawdown = 0

        # Expectancy = (average $ winners * win % + average $ losers * lose %) / (−average $ losers)
        tharp_expectancy = (net_profit / total_trades) / -average_loser


        print("\n###################\n")
        print("Performance Analysis :")
        print("HOLD and WAIT : ", self.sell_orders[-1] - self.buy_orders[0])
        print("Net Profit : ", net_profit)
        print("Gross Profit : ", gross_profit)
        print("Gross Loss   : ", gross_loss)
        print("Profit Factor : ", profit_factor)
        print()
        print("Total Number of Trades :", total_trades)
        print("Winning Trades :", number_profit_trades)
        print("Losing Trades :", number_loss_trades)
        print()
        print("Percent Profitable : ", (number_profit_trades / total_trades) * 100)
        print("Average Trade Net Profit : ", net_profit / total_trades)
        print("Average Winning Trade :", average_winner)
        print("Average Losing Trade : ", average_loser)
        print()
        print("Max Drawdown : ", max_drawdown)
        print("Net Profit as % of Max Drawdown : ", (net_profit / -max_drawdown) * 100)
        print()
        print("Tharp Expectancy: ", tharp_expectancy)
        print("\n###################\n")



        print("\nLosing Trades :")
        for trade_number in range(len(loss_trades)):
            print("Buy:" + str(loss_trades[trade_number][0]) + ", Sell:" + str(
                loss_trades[trade_number][1]) + " = " + str(
                loss_trades[trade_number][1] - loss_trades[trade_number][0]))

        print("\nProfitable Trades :")
        for trade_number in range(len(profit_trades)):
            print("Buy:" + str(profit_trades[trade_number][0]) + ", Sell:" + str(
                profit_trades[trade_number][1]) + " = " + str(
                profit_trades[trade_number][1] - profit_trades[trade_number][0]))

    def plot_equity_curve(self):

        #Create Equity cureve line
        investment_progression = list()
        investment = self.buy_orders[0]
        investment_progression.append(investment)
        for trade_number in range(len(self.sell_orders)):
            profit_loss = self.sell_orders[trade_number] - self.buy_orders[trade_number]
            investment += profit_loss
            investment_progression.append(investment)

        numpy_investment_series = numpy.array(investment_progression)
        numpy_investment_series = (numpy_investment_series/self.buy_orders[0])*100 - 100
        #
        plt.rc('axes', grid=True)
        plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5, alpha=1)
        plt.title("Equity Curve")
        plt.ylabel("Profit/Loss")
        plt.xlabel("No. of Trades")
        plt.plot(numpy_investment_series)

        plt.axhline(0,color="red" , lw=0.5)
        plt.show()




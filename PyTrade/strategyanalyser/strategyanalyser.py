class StrategyAnalyser():

    def __init__(self):
        self.buy_price = list()
        self.sell_price = list()

    def add_trade(self, bought_at=None, sold_at=None):
        """
        Add bew buy and sell trade.
        :param bought_at:
        :param sold_at:
        :return:
        """
        # Only add if previous trade is closed.
        if bought_at is not None and len(self.buy_price) == len(self.sell_price):
            self.buy_price.append(bought_at)
        # Only add if previous trade is open.
        if sold_at is not None and len(self.sell_price) == (len(self.buy_price) - 1):
            self.sell_price.append(sold_at)

    @property
    def buy_hold_amount(self):
        return self.sell_price[-1] - self.buy_price[0]

    @property
    def total_profit(self):
        total_profit = 0
        for trade in zip(self.sell_price, self.buy_price):
            total_profit += trade[0] - trade[1]
        return total_profit

    @property
    def total_trades(self):
        return len(self.sell_price)

    @property
    def profit_per_trade(self):
        return self.total_profit/self.total_trades

    def print_all_trades(self):
        print("All Trades are: \n")
        for trade in zip(self.sell_price, self.buy_price):
            print ("Buy: " + str(trade[1]) +", Sell: " +str(trade[0]))







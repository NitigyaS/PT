import sqlite3


class Broker:

    def __init__(self,db_name):
        self.db_name = "/tmp/"+db_name+".db"
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:

            c.execute('''CREATE TABLE trades
                     (date REAL, trans TEXT, symbol TEXT, qty REAL, price REAL)''')

        # Insert a row of data
        # Save (commit) the changes

        except sqlite3.OperationalError :
            print ("Table Already exisited. ")
            c.execute('''DELETE FROM trades;''')
            print("delete all old data. ")

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.commit()
        conn.close()

    def place_order(self, date, transaction_type, symbol, quantity, price):

        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        # Insert a row of data
        query = "INSERT INTO trades VALUES(" + str(date) + ",'" + transaction_type + "','" + symbol + "'," + str(quantity) + "," + str(price) + ")"
        c.execute(query)


        # Save (commit) the changes
        conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()

    def cancel_order(self,order_id):
        pass


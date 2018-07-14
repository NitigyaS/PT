import unittest

from sphinx.ext.napoleon import iterators

from PyTrade.feeds.CSVFeed import CSVFeed
from PyTrade.feeds.RandomFeed import RandomFeed
from conf.config import Config


class FeedTest(unittest.TestCase):

    def setUp(self):
        """Execute prior to each test"""
        self.config = Config("TEST")

    def tearDown(self):
        """Execute after each test"""
        pass

    #########
    # Tests #
    #########

    def test_environment(self):
        """Tests if current environment is test"""
        self.assertEqual(self.config.env, "Test")

    def test_rand_historic_data_size(self):
        """RandomFeed: tests if historic bar returns correct number of bars. """
        random_feed = RandomFeed("TCS", "NSE")
        historic_bar = random_feed.get_historical_data('01/07/2017', '21/07/2017')
        self.assertEqual(20, len(historic_bar["data"]))

    def test_rand_data_format(self):
        """CSVFeed: tests if live_feed returns is a generator and keys are okay"""
        random_feed = RandomFeed("TCS", "NSE")
        feed_data1 = random_feed.get_live_feed().__next__()
        self.assertIsInstance(feed_data1["data"]["open"], float)
        self.assertIsInstance(feed_data1["data"]["close"], float)
        self.assertIsInstance(feed_data1["data"]["low"], float)
        self.assertIsInstance(feed_data1["data"]["high"], float)
        self.assertIsInstance(feed_data1["data"]["volume"], int)
        self.assertIsInstance(feed_data1["data"]["timestamp"], float)

    def test_csv_live_feed(self):
        """CSVFeed: tests if live_feed returns is a generator and keys are okay"""
        csv_feed = CSVFeed("TCS", "NSE")
        feed_data1 = csv_feed.get_live_feed().__next__()
        self.assertIsInstance(feed_data1["data"]["open"], float)
        self.assertIsInstance(feed_data1["data"]["close"], float)
        self.assertIsInstance(feed_data1["data"]["low"], float)
        self.assertIsInstance(feed_data1["data"]["high"], float)
        self.assertIsInstance(feed_data1["data"]["volume"], int)
        self.assertIsInstance(feed_data1["data"]["timestamp"], float)

    def test_csv_historic_data_size(self):
        """CSVFeed: tests if historic bar returns correct number of bars. """
        csv_feed = CSVFeed("TCS", "NSE")
        historic_bar = csv_feed.get_historical_data('01/07/2017','21/07/2017')
        self.assertEqual(20, len(historic_bar["data"]))


if __name__ == "__main__":
    unittest.main()

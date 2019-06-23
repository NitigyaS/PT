import unittest

from PyTrade.feeds.CSVFeed import CSVFeed
from PyTrade.serializer.numpyserializer import NumpySerializer
from PyTrade.strategyanalyser.walkforward import WalkForward
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

    def test_set_parameters(self):
        wf = WalkForward()
        wf.set_parameters(para1=range(1, 5), para2=range(2, 4), para3=range(11, 21))
        number_of_parameter = wf.get_parameters()
        self.assertEqual(80, len(number_of_parameter))

    def test_set_data(self):
        number_of_samples = 10
        in_sample_size = 3
        out_sample_size = 1
        csv_feed = CSVFeed("TCS", "NSE")
        feed = csv_feed.get_historical_data("01/07/2017", "11/10/2017")

        # Create a Serializer convert csv data to numpy
        numpy_serializer = NumpySerializer(feed["data"])
        feed_data = numpy_serializer.get_series()
        wf = WalkForward()
        wf.set_data(feed_data , number_of_samples, in_sample_size, out_sample_size)
        sample_data = wf.get_sample_data()

        # Check Total number of sample generated.
        self.assertEqual((number_of_samples - in_sample_size - out_sample_size + 1), len(sample_data))

        # Check in_sample_length is triple of out_sample_length
        last_index = len(sample_data) - 1
        self.assertEqual(len(sample_data[last_index][0]), 3*len(sample_data[last_index][1]))


if __name__ == "__main__":
    unittest.main()
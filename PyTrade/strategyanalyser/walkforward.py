import itertools
from math import floor

from PyTrade.feeds.CSVFeed import CSVFeed
from PyTrade.serializer.numpyserializer import NumpySerializer


class WalkForward():

    def __init__(self):
        self.feed_data = None
        self.parameter_combinations = dict()
        self.sample_lists = list()

    def set_data(self, data, number_of_samples=10, in_sample_size=3, out_sample_size=1):
        self.feed_data = data
        length_sub_array = floor(len(self.feed_data)/number_of_samples)

        total_number_sample = number_of_samples - in_sample_size - out_sample_size + 1
        # Create Sample List
        for sample_number in range(total_number_sample):
            start_index_in_sample = sample_number*length_sub_array
            end_index_in_sample = (sample_number + in_sample_size)*length_sub_array
            in_sample_data = self.feed_data[start_index_in_sample : end_index_in_sample]
            start_index_out_sample = (sample_number + in_sample_size)*length_sub_array
            end_index_out_sample = (sample_number + in_sample_size + out_sample_size)*length_sub_array
            out_sample_data = self.feed_data[start_index_out_sample : end_index_out_sample]
            self.sample_lists.append((in_sample_data, out_sample_data))

    def get_sample_data(self):
        return self.sample_lists

    def set_parameters(self, **kwargs):
        """
        Provide range of parameter
        :param kwargs: pass parameter in the form parameter_name = (range of values)
        :return: [{'para1':v1, 'para2':v2 }, {'para1':v3, 'para2':v4}]
        """
        input_parameters_range = list(kwargs.values())
        combination_parameter = list(itertools.product(*input_parameters_range))
        self.parameter_combinations = [ dict(zip(kwargs.keys(),combination)) for combination in combination_parameter]

    def get_parameters(self):
        return self.parameter_combinations

    def analyse(self):
        pass


if __name__ == '__main__':
    wf = WalkForward()
    #wf.set_parameters(para1=range(2,5) , para2=range(10,14),para3=range(22,25) ,para4=range(32,35))
    csv_feed = CSVFeed("TCS", "NSE")
    feed = csv_feed.get_historical_data("01/07/2017", "11/10/2017")

    # Create a Serializer convert csv data to numpy
    numpy_serializer = NumpySerializer(feed["data"])
    feed_data = numpy_serializer.get_series()
    wf.set_data(feed_data)


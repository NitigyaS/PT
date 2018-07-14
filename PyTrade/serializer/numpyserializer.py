from PyTrade.serializer.serializer import Serializer
import numpy


class NumpySerializer(Serializer):
    """
    inherits the Serializer class. To create a Numpy Series
    """

    def __init__(self, barlist=None, size=30):
        super().__init__(barlist, size)
        self.barlist_to_series()

    def barlist_to_series(self):
        """
        converts the list of dict{"open":100, "close":100, "high":100, "low":100, "volume":100}
        to a numpy.ndarray
        :return:
        """
        self.series = numpy.array([(data["open"],
                                    data["close"],
                                    data["low"],
                                    data["high"],
                                    data["volume"],
                                    data["timestamp"]) for data in self.barlist],
                                  dtype=[
                                      ('open', float),
                                      ('close', float),
                                      ('low', float),
                                      ('high', float),
                                      ('volume', int),
                                      ('timestamp', int)
                                  ])

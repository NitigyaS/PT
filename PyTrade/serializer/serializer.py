from abc import ABC, abstractmethod


class Serializer(ABC):
    """Serializer class to be inherited by other classes in serializer"""

    def __init__(self, barlist=None, size=None):
        """
        Initialization Method
        :param barlist: list() of dicts {"open":100, "close":100, "high":100, "low":100, "volume":100}
        :param size: max_size allowed of series
        """
        self.size = size
        self.series = None
        if type(barlist) is list:
            self.barlist = barlist
        elif barlist is None:
            self.barlist = list()
        else:
            raise UnrecognizedSeriesException(1,"barlist is not a list of bar data. ")

    def add_bar(self, new_bar):
        """
        Method add the new_bar to existing series.
        :return:
        """
        if type(new_bar) is not dict:
            raise UnrecognizedSeriesException(2,"new_bar is not a dict. ")

        self.barlist.append(new_bar)
        if self.size is not None:
            self.barlist = self.barlist[-self.size:]
        self.barlist_to_series()
        return self.get_series()

    @abstractmethod
    def barlist_to_series(self):
        """
        Method converts the data received from Feed class to series.
        :return:
        """
        pass

    def get_series(self):
        """
        Method returns the series implementation of feed data.
        :return: series
        """
        return self.series


class UnrecognizedSeriesException(Exception):
    """Exception class for Series"""
    def __init__(self,error_no,msg):
        self.args = (error_no, msg)
        self.error_no = error_no
        self.msg = msg
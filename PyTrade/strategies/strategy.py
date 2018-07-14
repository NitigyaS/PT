from abc import ABC, abstractmethod


class Strategy(ABC):
    """Class is inherited by other class implementing strategy. """

    def __init__(self):
        self.__enter = False
        self.__exit = False

    def should_enter(self):
        """

        :return:
        Returns True if strategy should enter. False Otherwise.
        """
        if self.__enter == self.__exit is True:
            raise StrategyFailedException(1, "Both enter and exit are True")
        return self.__enter

    def should_exit(self):
        """

        :return:
        Returns True if strategy should exit. False Otherwise.
        """
        if self.__enter == self.__exit is True:
            raise StrategyFailedException(1, "Both enter and exit are True")
        return self.__exit

    @abstractmethod
    def evaluate(self, numpy_array):
        """Evaluates the numpy recarray and set the self.enter and self.exit booleans. """
        pass

    def set_states(self, enter_strategy=False, exit_strategy=False):
        """
        :param enter_strategy: True if strategy should entered. False Otherwise.
        :param exit_strategy: True if strategy shodl exited. False Otherwise.
        :return:
        None
        """
        self.__exit = exit_strategy
        self.__enter = enter_strategy


class StrategyFailedException(Exception):
    """
    Exception Class for Strategy.
    """

    def __init__(self, error_no, msg):
        self.args = (error_no, msg)
        self.error_no = error_no
        self.msg = msg


class StrategyNotReady(Exception):
    """
    Exception Class for Strategy.
    """

    def __init__(self, error_no, msg):
        self.args = (error_no, msg)
        self.error_no = error_no
        self.msg = msg

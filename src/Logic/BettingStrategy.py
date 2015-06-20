####################
#
# BettingStrategy.py
#
####################

from abc import ABCMeta, abstractmethod

class BettingStrategy(metaclass=ABCMeta):
    """Base class for betting policies"""

    @abstractmethod
    def bet(self):
        """Returns amount to wager"""
        pass

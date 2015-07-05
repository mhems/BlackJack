####################
#
# BettingStrategy.py
#
####################

from abc import ABCMeta, abstractmethod

class BettingStrategy(metaclass=ABCMeta):
    """Base class for betting policies"""

    @abstractmethod
    def bet(self, **kwargs):
        """Returns amount to wager"""
        raise NotImplementedError(
            'BettingStrategy implentations must implement the bet method')

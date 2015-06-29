####################
#
# Hand.py
#
####################

from abc import ABCMeta, abstractmethod

class Hand(metaclass=ABCMeta):
    """Abstract base class for card hands"""

    @abstractmethod
    def value(self):
        """Returns largest value of hand"""
        pass

    @abstractmethod
    def numCards(self):
        """Returns number of cards in hand"""
        pass

    @abstractmethod
    def addCards(self, cards):
        """Adds list of cards to hand"""
        pass

    @abstractmethod
    def reset(self):
        """Resets hand to have no cards"""
        pass

    @abstractmethod
    def __str__(self):
        """Returns canonical representation of hand"""
        pass

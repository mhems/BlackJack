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
        raise NotImplementedError(
            'Hand implementations must implement the value method')

    @abstractmethod
    def numCards(self):
        """Returns number of cards in hand"""
        raise NotImplementedError(
            'Hand implementations must implement the numCards method')

    @abstractmethod
    def addCards(self, cards):
        """Adds list of cards to hand"""
        raise NotImplementedError(
            'Hand implementations must implement the addCards method')

    @abstractmethod
    def reset(self):
        """Resets hand to have no cards"""
        raise NotImplementedError(
            'Hand implementations must implement the reset method')

    @abstractmethod
    def __str__(self):
        """Returns canonical representation of hand"""
        raise NotImplementedError(
            'Hand implementations must implement the __str__ method')

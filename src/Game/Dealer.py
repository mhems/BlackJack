####################
#
# Dealer.py
#
####################

from src.Game.HouseBank     import HouseBank
from src.Logic.DealerPolicy import DealerPolicy

class Dealer:
    """Representation of blackjack dealer"""

    def __init__(self, name = 'Dealer'):
        """Initializes Dealer members"""
        self.name   = name
        self.__hand = None
        self.__isActive = True
        self.__policy = DealerPolicy()
        self.__stack = HouseBank()

    @property
    def stackAmount(self):
        """Returns amount of money in house bank"""
        return self.__stack.amount

    def act(self, hand, upcard, availableCommands):
        """Returns command player wishes to execute based on its policy"""
        return self.__policy.decide(hand, upcard, availableCommands)

    def __eq__(self, other):
        """Returns True iff player is other"""
        return id(self) == id(other)

    def __str__(self):
        """Returns string representation of player"""
        return '%s has $%d' % (self.name, self.stackAmount)

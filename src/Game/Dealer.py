####################
#
# Dealer.py
#
####################

from src.Logic.DealerPolicy import DealerPolicy

class Dealer:
    """Representation of blackjack dealer"""

    def __init__(self, name = 'Dealer'):
        """Initializes Dealer members"""
        self.name   = name
        self.__hand = None
        self.__isActive = True
        self.__policy = DealerPolicy()

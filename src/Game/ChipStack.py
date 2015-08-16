####################
#
# ChipStack.py
#
####################

from src.Game.Bank import Bank
from src.Game.Bank import InsufficientFundsError

class ChipStack(Bank):
    """Representation of player's chip stack"""

    def __init__(self):
        """Initializes ChipStack"""
        self.__funds = 0

    @property
    def amount(self):
        """Returns amount of funds"""
        return self.__funds

    def withdraw(self, amt):
        """Attempts to withdraw amt from funds"""
        """If there are less than amt in funds, returns None"""
        if amt <= self.__funds:
            self.__funds -= amt
            return amt
        else:
            raise InsufficientFundsError(amt, self.__funds)

    def deposit(self, amt):
        """Deposits amt into funds"""
        if amt > 0:
            self.__funds += amt

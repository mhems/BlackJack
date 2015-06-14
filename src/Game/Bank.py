####################
#
# Bank.py
#
####################

from abc import ABCMeta, abstractmethod, abstractproperty

class Bank:
    """Abstract mechanism for Bank transactions"""

    @abstractmethod
    def __init__(self):
        """Initializes funds"""
        pass

    @abstractmethod
    def withdraw(self, amt):
        """Attempts to withdraw amt from funds"""
        pass

    @abstractmethod
    def deposit(self, amt):
        """Deposits amt into funds"""
        pass

    @abstractproperty
    def amount(self):
        """Returns amount in funds"""
        pass

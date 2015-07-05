####################
#
# Bank.py
#
####################

from abc import ABCMeta, abstractmethod, abstractproperty

class Bank:
    """Abstract mechanism for Bank transactions"""

    @abstractproperty
    def amount(self):
        """Returns amount in funds"""
        raise NotImplementedError(
            'Bank implementations must implement the amount property')
    
    @abstractmethod
    def withdraw(self, amt):
        """Attempts to withdraw amt from funds"""
        raise NotImplementedError(
            'Bank implementations must implement the withdraw method')

    @abstractmethod
    def deposit(self, amt):
        """Deposits amt into funds"""
        raise NotImplementedError(
            'Bank implementations must implement the deposit method')

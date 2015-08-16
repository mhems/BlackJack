####################
#
# Bank.py
#
####################

from abc import ABCMeta, abstractmethod, abstractproperty

class InsufficientFundsError(Exception):
    """Error class to represent error of overwithdrawing from bank"""

    def __init__(self, request, balance):
        self.request = request
        self.balance = balance

    def __str__(self):
        return 'Insufficient funds to withdraw $%s from $%s' % (self.request, self.balance)

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

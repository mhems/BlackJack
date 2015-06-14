####################
#
# HouseBank.py
#
####################

class HouseBank(Bank):
    """Representation of Casino House Bank"""

    def __init__(self):
        """Initializes funds"""
        self.__funds = 0

    def withdraw(self, amt):
        """Withdraws amt from funds"""
        # The House has "infinite" bankroll
        self.__funds -= amt
        return amt;

    def deposit(self, amt):
        """Deposits amt into funds"""
        self.__funds += amt

    def amount(self):
        """Returns amount of funds"""
        return self.__funds

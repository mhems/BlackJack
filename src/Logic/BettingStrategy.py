import re
from abc import ABCMeta, abstractmethod

import src.Utilities.Configuration as config

class BettingStrategy(metaclass=ABCMeta):
    """Base class for betting policies"""

    @abstractmethod
    def bet(self, **kwargs):
        """Returns amount to wager"""
        raise NotImplementedError(
            'BettingStrategy implentations must implement the bet method')

class HumanInputBettingStrategy(BettingStrategy):
    """Policy to bet based on inputted amount"""

    def bet(self, **kwargs):
        """Bets according to human input"""
        result = input('Enter your bet amount: ')
        while not re.match(r'[1-9][0-9]+', result):
            print('Bet must be positive integer')
            result =input('Enter your bet amount: ')
        return result

class MinBettingStrategy(BettingStrategy):
    """Policy to always bet table minimum"""

    def bet(self, **kwargs):
        """Return minimum bet allowed"""
        return config.get('MINIMUM_BET')

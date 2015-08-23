####################
#
# MinBettingStrategy.py
#
####################

from src.Logic.BettingStrategy   import BettingStrategy
import src.Utilities.Configuration as config

class MinBettingStrategy(BettingStrategy):
    """Policy to always bet table minimum"""

    def bet(self, **kwargs):
        """Return minimum bet allowed"""
        return config.get('MINIMUM_BET')

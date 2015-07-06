####################
#
# MinBettingStrategy.py
#
####################

from src.Logic.BettingStrategy   import BettingStrategy
from src.Utilities.Configuration import Configuration

class MinBettingStrategy(BettingStrategy):
    """Policy to always bet table minimum"""

    def bet(self, **kwargs):
        """Return minimum bet allowed"""
        return Configuration.get('MINIMUM_BET')

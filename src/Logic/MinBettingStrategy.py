####################
#
# MinBettingStrategy.py
#
####################

from src.Logic.BettingStrategy import BettingStrategy

class MinBettingStrategy(BettingStrategy):
    """Policy to always bet table minimum"""

    def bet(self, **kwargs):
        return Configuration.get('MIN_BET')

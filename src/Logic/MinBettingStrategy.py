####################
#
# MinBettingStrategy.py
#
####################

class MinBettingStrategy(BettingStrategy):
    """Policy to always bet table minimum"""

    def bet(self):
        return Configuration.configuration['MIN_BET']

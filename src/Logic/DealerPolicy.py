####################
#
# DealerPolicy.py
#
####################

from src.Logic.Command        import Command
from src.Logic.DecisionPolicy import DecisionPolicy
from src.Utilities.Configuration import Configuration

class DealerPolicy(DecisionPolicy):
    """Class for blackjack Dealer's decision policy"""

    def decide(self, hand, upcard, availabeCommands, **kwargs):
        """Decides command according to dealer rules"""
        hitS17 = hand.isSoft17 and Configuration.get('DEALER_HITS_ON_SOFT_17')
        if hand.value < 17 or hitS17:
            return Command.getCommand('H')
        else:
            return Command.getCommand('S')

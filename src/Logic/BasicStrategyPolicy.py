####################
#
# BasicStrategyPolicy.py
#
####################

from src.Logic.StrategyChart  import StrategyChart
from src.Logic.Command        import Command
from src.Logic.DecisionPolicy import DecisionPolicy

class BasicStrategyPolicy(DecisionPolicy):
    """Represents use of basic strategy to inform actions"""

    def __init__(self, filename):
        self.strategy = StrategyChart.fromFile(filename)

    def decide(self, hand, upcard, availableCommands, **kwargs):
        """Decides command based on basic strategy"""
        upvalue = 'A' if upcard.isAce else upcard.value
        print(upvalue)
        p = self.strategy.advise(hand, upvalue, availableCommands)
        print('decide',p)
        return p

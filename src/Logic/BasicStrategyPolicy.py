####################
#
# BasicStrategyPolicy.py
#
####################

from src.Logic.Command        import Command
from src.Logic.DecisionPolicy import DecisionPolicy

class BasicStrategyPolicy(DecisionPolicy):
    """Represents use of basic strategy to inform actions"""

    def __init__(self, filename):
        self.strategy = StrategyChart.fromFile(filename)

    def decide(self, hand, upcard, availableCommands, **kwargs):
        """Decides command based on basic strategy"""
        command = self.strategy.advise(self, hand, upcard)
        if command[0].upper() == 'D'and len(command) == 2:
            if Command.DOUBLE_ENUM in availableCommands:
                return Command.DOUBLE_ENUM
            else:
                if command[1].upper() == 'H':
                    return Command.HIT_ENUM
                elif command[1].upper() == 'S':
                    return Command.STAND_ENUM
        else:
            return command

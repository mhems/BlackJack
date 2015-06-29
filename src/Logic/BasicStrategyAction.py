####################
#
# BasicStrategyAction.py
#
####################

class BasicStrategyAction(Action):
    """Represents use of basic strategy to inform actions"""

    def __init__(self, filename):
        self.strategy = StrategyChart.fromFile(filename)

    def act(self, hand, upcard):
        """Acts based on basic strategy"""
        advice = self.strategy.advise(self, hand, upcard)
        return Command.getCommand(advice.upper())

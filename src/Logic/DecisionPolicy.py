from abc import ABCMeta, abstractmethod

from src.Logic.StrategyChart import StrategyChart
from src.Logic.Command import Command
from src.Utilities.Utilities import LINE_END
import src.Utilities.Configuration as config

class DecisionPolicy(metaclass=ABCMeta):
    """Base class for decision policies on how to act"""

    @abstractmethod
    def decide(self, hand, upcard, availableCommands, **kwargs):
        """Returns Command that policy wishes to execute"""
        raise NotImplementedError(
            'DecisionPolicy implementations must implement the act method')

class BasicStrategyPolicy(DecisionPolicy):
    """Represents use of basic strategy to inform actions"""

    def __init__(self, filename):
        self.strategy = StrategyChart.fromFile(filename)

    def decide(self, hand, upcard, availableCommands, **kwargs):
        """Decides command based on basic strategy"""
        upvalue = 'A' if upcard.isAce else upcard.value
        return self.strategy.advise(hand, upvalue, availableCommands)

class DealerPolicy(DecisionPolicy):
    """Class for blackjack Dealer's decision policy"""

    def decide(self, hand, upcard, availabeCommands, **kwargs):
        """Decides command according to dealer rules"""
        hitS17 = hand.isSoft17 and config.get('DEALER_HITS_ON_SOFT_17')
        if hand.value < 17 or hitS17:
            return Command.getCommandEnumFromString('H')
        else:
            return Command.getCommandEnumFromString('S')

class FeedbackDecisionPolicy(DecisionPolicy):
    """Represents use of human input with basic strategy
       used to advise player after decision"""

    def __init__(self, input_policy, strategy_policy):
        """Initializes members"""
        self.input_policy = input_policy
        self.strategy_policy = strategy_policy
        self.num_wrong = 0

    def decide(self, hand, upcard, availableCommands, **kwargs):
        """First corrects player's decision if wrong, then
           returns Command that policy wishes to execute"""
        decision = self.input_policy.decide(hand,
                                            upcard,
                                            availableCommands,
                                            **kwargs)
        expected = self.strategy_policy.decide(hand,
                                               upcard,
                                               availableCommands,
                                               **kwargs)
        if decision != expected and expected in availableCommands:
            self.num_wrong += 1
            print( 'WRONG: You %s when you should have %s' %
                   ( Command.getPastTenseCommandName(decision),
                     Command.getPastTenseCommandName(expected) ) )
        return decision

class HumanInputPolicy(DecisionPolicy):
    """Class to prompt human for decision"""

    def decide(self, hand, upcard, availableCommands, **kwargs):
        """Decides according to human input"""

        def prompt(availableCommands):
            """Prompts for response"""
            response = input( ('How will you act? Options = %s' + LINE_END) %
                              ( ', '.join( ( Command.getCommandStringFromEnum(e)
                                             for e in availableCommands ) ) ) )
            return Command.getCommandEnumFromString(response), response

        print('Your hand (%s) has value %d, Dealer shows %s' % (hand.ranks,
                                                                hand.value,
                                                                upcard))
        command, response = prompt(availableCommands)
        while command is None:
            print('Unknown or unavailable action: %s' % response)
            command, response = prompt(availableCommands)
        return command

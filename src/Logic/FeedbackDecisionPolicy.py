####################
#
# FeedbackDecisionPolicy.py
#
####################

from src.Logic.Command import Command
from src.Logic.DecisionPolicy import DecisionPolicy

class FeedbackDecisionPolicy(DecisionPolicy):
    """Represents use of human input with basic strategy
       used to advise player after decision"""

    def __init__(self, input_policy, strategy_policy):
        """Initializes members"""
        self.__input_policy    = input_policy
        self.__strategy_policy = strategy_policy
    
    def decide(self, hand, upcard, availableCommands, **kwargs):
        """First corrects player's decision if wrong, then
           returns Command that policy wishes to execute"""
        decision = self.__input_policy.decide(hand,
                                              upcard,
                                              availableCommands,
                                              **kwargs)
        expected = self.__strategy_policy.decide(hand,
                                                 upcard,
                                                 availableCommands,
                                                 **kwargs)
        if decision != expected and expected in availableCommands:
            print( 'WRONG: You %s when you should have %s' %
                   ( Command.getPastTenseCommandName(decision),
                     Command.getPastTenseCommandName(expected) ) )
        return decision

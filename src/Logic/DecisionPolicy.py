####################
#
# DecisionPolicy.py
#
####################

from abc import ABCMeta, abstractmethod

class DecisionPolicy(metaclass=ABCMeta):
    """Base class for decision policies on how to act"""

    @abstractmethod
    def decide(self, hand, upcard, availableCommands, **kwargs):
        """Returns Command that policy wishes to execute"""
        raise NotImplementedError(
            'Action implementations must implement the act method')

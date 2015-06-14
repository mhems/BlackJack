####################
#
# Action.py
#
####################

from abc import ABCMeta, abstractmethod

from src.Utilities.Configuration import Configuration

class Action(metaclass=ABCMeta):
    """Base class for action policies"""

    @abstractmethod
    def act(self, hand, upcard):
        pass

####################
#
# Action.py
#
####################

from abc import ABCMeta, abstractmethod

class Action(metaclass=ABCMeta):
    """Base class for action policies"""

    @abstractmethod
    def act(self, hand, upcard):
        pass

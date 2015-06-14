####################
#
# Command.py
#
####################

from abc import ABCMeta, abstractmethod

HIT          = 3
STAND        = 4
SPLIT        = 5
DOUBLE_HIT   = 6
DOUBLE_STAND = 7
SURRENDER    = 8

command_map = {
    'H'  : Command.HIT,
    'S'  : Command.STAND,
    'SP' : Command.SPLIT,
    'D'  : Command.DOUBLE,
    'DH' : Command.DOUBLE_HIT,
    'DS' : Command.DOUBLE_STAND,
    'SU' : Command.SURRENDER,
    'ES' : Command.EARLY_SURRENDER
}

class Command(metaclass=ABCMeta):
    """Base class for Blackjack commands"""

    @abstractmethod
    def perform(self):
        """Perform command"""
        pass

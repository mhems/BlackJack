####################
#
# Command.py
#
####################

from abc import ABCMeta, abstractmethod

class Command(metaclass=ABCMeta):
    """Base class for Blackjack commands"""

    HIT          = 3
    STAND        = 4
    SPLIT        = 5
    DOUBLE_HIT   = 6
    DOUBLE_STAND = 7
    SURRENDER    = 8

    __command_map = {
        'H'  : Command.HIT,
        'S'  : Command.STAND,
        'SP' : Command.SPLIT,
        'D'  : Command.DOUBLE,
        'DH' : Command.DOUBLE_HIT,
        'DS' : Command.DOUBLE_STAND,
        'SU' : Command.SURRENDER,
        'ES' : Command.EARLY_SURRENDER
    }
    
    @abstractmethod
    def perform(self):
        """Perform command"""
        pass

    @abstractmethod
    def __str__(self):
        """Returns string representing Command"""
        pass

    @abstractmethod
    def __repr__(self):
        """Returns representation of Command"""
        pass
    
    @staticmethod
    def getCommand(string):
        """Returns Command number from string representation"""
        return Command.__command_map[string] if string in Command.__command_map else None

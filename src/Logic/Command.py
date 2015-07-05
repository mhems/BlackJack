####################
#
# Command.py
#
####################

from abc import ABCMeta, abstractmethod
from src.Utilities.Enum import Enum

class Command(metaclass=ABCMeta):
    """Base class for Blackjack commands"""

    HIT_ENUM    = Enum()
    STAND_ENUM  = Enum()
    DOUBLE_ENUM = Enum()
    SPLIT_ENUM  = Enum()

    __command_map = {
        'HIT'    : HIT_ENUM,
        'H'      : HIT_ENUM,
        'STAND'  : STAND_ENUM,
        'S'      : STAND_ENUM,
        'DOUBLE' : DOUBLE_ENUM,
        'D'      : DOUBLE_ENUM,
        'SPLIT'  : SPLIT_ENUM,
        'SP'     : SPLIT_ENUM
    }
    
    def execute(self, slot, **kwargs):
        """Executes the command on slot,
           Return True iff player is done with turn"""
        if not self.isAvailable():
            raise UnavailableCommandException(
                '%s command is unavailable' % str(self))
        return self.__perform(slot, **kwargs)

    @abstractmethod
    def __perform(self, slot, **kwargs):
        """Perform command on slot,
           Return True iff player is done with turn"""
        raise NotImplementedError(
            'Command implementations must implement the __perform method')

    @abstractmethod
    def isAvailable(self, slot):
        """Returns True iff command is permitted for slot's player and hand"""
        raise NotImplementedError(
            'Command implementations must implement the isAvailable method')
        
    @abstractmethod
    def __str__(self):
        """Returns string representing Command"""
        raise NotImplementedError(
            'Command implementations must implement the __str__ method')

    @abstractmethod
    def __repr__(self):
        """Returns representation of Command"""
        raise NotImplementedError(
            'Command implementations must implement the __repr__ method')
    
    @staticmethod
    def getCommand(string):
        """Returns Command number from string representation"""
        s = string.upper()
        return Command.__command_map[s] if s in Command.__command_map else None

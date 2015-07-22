####################
#
# Command.py
#
####################

from abc import ABCMeta, abstractmethod
from src.Utilities.Utilities import Utilities

class UnavailableCommandError(Exception):
    """Exception signifying unavailable command attempted to execute"""
    pass

class Command(metaclass=ABCMeta):
    """Base class for Blackjack commands"""

    HIT_ENUM       = Utilities.uniqueNumber()
    STAND_ENUM     = Utilities.uniqueNumber()
    DOUBLE_ENUM    = Utilities.uniqueNumber()
    SPLIT_ENUM     = Utilities.uniqueNumber()
    SURRENDER_ENUM = Utilities.uniqueNumber()
    
    __command_string_map = {
        # Order duplicate entries by descending string length
        'HIT'       : HIT_ENUM,
        'H'         : HIT_ENUM,
        'STAND'     : STAND_ENUM,
        'S'         : STAND_ENUM,
        'DOUBLE'    : DOUBLE_ENUM,
        'D'         : DOUBLE_ENUM,
        'SPLIT'     : SPLIT_ENUM,
        'SP'        : SPLIT_ENUM,
        'SURRENDER' : SURRENDER_ENUM,
        'SU'        : SURRENDER_ENUM
    }

    # Thanks to Emil @ stackoverflow.com/questions/3318625
    #   for his succinct approach to bidirectional mapping
    # Note this assumes no commands are inserted dynamically
    __command_enum_map = dict( ( reversed(item)
                                 for item in
                                 __command_string_map.items()
                                 if len(item[0]) > 2 ) )

    __past_tense_command_map = {
        HIT_ENUM       : 'HIT',
        STAND_ENUM     : 'STOOD',
        DOUBLE_ENUM    : 'DOUBLED',
        SPLIT_ENUM     : 'SPLIT',
        SURRENDER_ENUM : 'SURRENDERED'
    }
    
    @staticmethod
    def getCommandEnumFromString(string):
        """Returns Command enum from string representation"""
        s = string.upper()
        if s in Command.__command_string_map:
            return Command.__command_string_map[s]
        else:
            return None

    @staticmethod
    def getCommandStringFromEnum(enum):
        """Returns Command string from enum representation"""
        if enum in Command.__command_enum_map:
            return Command.__command_enum_map[enum]
        else:
            return None
    
    @staticmethod
    def getPastTenseCommandName(enum):
        """Returns past tense of command from enum"""
        if enum in Command.__past_tense_command_map:
            return Command.__past_tense_command_map[enum]
        else:
            return None
    
    def execute(self, slot, **kwargs):
        """Executes the command on slot,
           Return True iff player is done with turn"""
        if not self.isAvailable(slot):
            raise UnavailableCommandError(
                '%s command is unavailable' % str(self))
        return self.perform(slot, **kwargs)

    @abstractmethod
    def perform(self, slot, **kwargs):
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

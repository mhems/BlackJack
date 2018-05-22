from abc import ABCMeta, abstractmethod
from src.Utilities.Utilities import Enum

class UnavailableCommandError(Exception):
    """Exception signifying unavailable command attempted to execute"""

    def __init__(self, command, slot):
        self.command = command
        self.slot = slot

    def __str__(self):
        return '%s is unavailable to %s' % (str(self.command),
                                            self.slot.playerName)

class Command(metaclass=ABCMeta):
    """Base class for Blackjack commands"""

    HIT_ENUM = Enum()
    STAND_ENUM = Enum()
    DOUBLE_ENUM = Enum()
    SPLIT_ENUM = Enum()
    SURRENDER_ENUM = Enum()

    command_string_map = {
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
    command_enum_map = dict( ( reversed(item)
                               for item in
                               command_string_map.items()
                               if len(item[0]) > 2 ) )

    past_tense_command_map = {
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
        if s in Command.command_string_map:
            return Command.command_string_map[s]
        return None

    @staticmethod
    def getCommandStringFromEnum(enum):
        """Returns Command string from enum representation"""
        if enum in Command.command_enum_map:
            return Command.command_enum_map[enum]
        return None

    @staticmethod
    def getPastTenseCommandName(enum):
        """Returns past tense of command from enum"""
        if enum in Command.past_tense_command_map:
            return Command.past_tense_command_map[enum]
        return None

    def execute(self, slot, **kwargs):
        """Executes the command on slot,
           Return True iff player is done with turn"""
        if not self.isAvailable(slot):
            raise UnavailableCommandError(self, slot)
        return self.perform(slot, **kwargs)

    @abstractmethod
    def perform(self, slot, **kwargs):
        """Perform command on slot,
           Return True iff player is done with turn"""
        raise NotImplementedError(
            'Command implementations must implement the perform method')

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

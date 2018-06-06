from abc import ABCMeta, abstractmethod

class UnavailableCommandError(Exception):
    """Exception signifying unavailable command attempted to execute"""

    def __init__(self, command, slot):
        super().__init__()
        self.command = command
        self.slot = slot

    def __str__(self):
        return '%s is unavailable to %s' % (str(self.command),
                                            self.slot.playerName)

class Command(metaclass=ABCMeta):
    """Base class for Blackjack commands"""

    HIT = 1
    STAND = 2
    DOUBLE = 3
    SPLIT = 4
    SURRENDER = 5

    commands = [HIT, STAND, DOUBLE, SPLIT, SURRENDER]

    command_to_string = {
        HIT : '(H)it',
        STAND : '(S)tand',
        DOUBLE : '(D)ouble',
        SPLIT : '(Sp)lit',
        SURRENDER : '(Su)rrender'
    }

    string_to_command = {
        'H' : HIT,
        'HIT' : HIT,
        'S' : STAND,
        'STAND' : STAND,
        'D' : DOUBLE,
        'DOUBLE' : DOUBLE,
        'SP' : SPLIT,
        'SPLIT' : SPLIT,
        'SU' : SURRENDER,
        'SURRENDER' : SURRENDER
    }

    command_to_past_tense = {
        HIT       : 'HIT',
        STAND     : 'STOOD',
        DOUBLE    : 'DOUBLED',
        SPLIT     : 'SPLIT',
        SURRENDER : 'SURRENDERED'
    }

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

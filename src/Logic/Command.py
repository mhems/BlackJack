from abc import ABCMeta, abstractmethod
from math import floor

import src.Utilities.Configuration as config

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

class HitCommand(Command):
    """Representation of hit action"""

    def __init__(self, shoe):
        """Initializes members"""
        self.shoe = shoe

    def perform(self, slot, **kwargs):
        """Perform Hit command"""
        slot.addCards(self.shoe.dealOneCard())
        return False

    def isAvailable(self, slot):
        """Returns True iff Hit command is available"""
        return True

    def __str__(self):
        """Returns string representing Hit Command"""
        return 'Hit'

    def __repr__(self):
        """Returns representation of Hit Command"""
        return 'H'

class StandCommand(Command):
    """Representation of the stand (stay) action"""

    def perform(self, slot, **kwargs):
        """Perform Stand command"""
        return True

    def isAvailable(self, _):
        """Stand is always available"""
        return True

    def __str__(self):
        """Returns string representing Stand Command"""
        return 'Stand'

    def __repr__(self):
        """Returns representation of Stand Command"""
        return 'S'

class DoubleCommand(Command):
    """Representation of the double down action"""

    def __init__(self, hitCommand, standCommand):
        """Initialize members"""
        self.hit_command = hitCommand
        self.stand_command = standCommand

    def perform(self, slot, **kwargs):
        """Perform Double command"""
        amt = floor(slot.pot * config.get('DOUBLE_RATIO'))
        slot.pots[slot.index] += slot.player.wager(amt)
        self.hit_command.execute(slot, **kwargs)
        return self.stand_command.execute(slot, **kwargs)

    def isAvailable(self, slot):
        """Double available depending on configuration"""
        if not slot.playerCanAffordDouble:
            return False
        if not slot.firstAction:
            return False
        double_range = config.get('TOTALS_ALLOWED_FOR_DOUBLE')
        if (double_range != config.UNRESTRICTED and
            not slot.hand.value in double_range):
            return False
        if (slot.hand.wasSplit and
            not config.get('DOUBLE_AFTER_SPLIT_ALLOWED')):
            return False
        return True

    def __str__(self):
        """Returns string representing Double Command"""
        return 'Double'

    def __repr__(self):
        """Returns representation of Double Command"""
        return 'D'

class SplitCommand(Command):
    """Representation of the split command"""

    def __init__(self, hitCommand, standCommand):
        """Initialize members"""
        self.hit_command = hitCommand
        self.stand_command = standCommand

    def perform(self, slot, **kwargs):
        """Perform Split command"""
        done = (slot.hand.isAcePair and
                not config.get('HIT_SPLIT_ACES') and
                not config.get('RESPLIT_ACES'))
        slot.splitHand()
        self.hit_command.execute(slot, **kwargs)
        slot.index += 1
        self.hit_command.execute(slot, **kwargs)
        slot.index -= 1
        return done

    def isAvailable(self, slot):
        """Returns True iff Split command is available"""
        if config.get('SPLIT_BY_VALUE'):
            toTest = slot.hand.isPairByValue
        else:
            toTest = slot.hand.isPairByRank
        if not toTest:
            return False
        if not slot.playerCanAffordSplit:
            return False
        if not slot.firstAction:
            return False
        num_splits_allowed = config.get('RESPLIT_UP_TO')
        if (num_splits_allowed != config.UNRESTRICTED and
            slot.numSplits + 1 >= num_splits_allowed):
            return False
        if (slot.hand.wasSplit and slot.hand.isAcePair and
            not config.get('RESPLIT_ACES')):
            return False
        return True

    def __str__(self):
        """Returns string representing Split Command"""
        return 'Split'

    def __repr__(self):
        """Returns representation of Split Command"""
        return 'Sp'

class SurrenderCommand(Command):
    """Representation of the (late) surrender action"""

    def perform(self, slot, **kwargs):
        """Perform Surrender command"""
        slot.surrendered = True
        return True

    def isAvailable(self, slot):
        """Returns True iff (late) surrender is available"""
        return config.get('LATE_SURRENDER') and slot.firstAction

    def __str__(self):
        """Returns string representing Surrender Command"""
        return 'Surrender'

    def __repr__(self):
        """Returns representation of Surrender Command"""
        return 'SU'

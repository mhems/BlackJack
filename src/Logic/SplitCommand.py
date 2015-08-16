####################
#
# SplitCommand.py
#
####################

from src.Logic.Command import Command
from src.Utilities.Configuration import Configuration

class SplitCommand(Command):
    """Representation of the split command"""

    def __init__(self, hitCommand, standCommand):
        """Initialize members"""
        self.__hit_command   = hitCommand
        self.__stand_command = standCommand
    
    def perform(self, slot, **kwargs):
        """Perform Split command"""
        done = (slot.handIsAcePair and
                not Configuration.get('HIT_SPLIT_ACES') and
                not Configuration.get('RESPLIT_ACES'))
        slot.splitHand()
        self.__hit_command.execute(slot, **kwargs)
        slot.index += 1
        self.__hit_command.execute(slot, **kwargs)
        slot.index -= 1
        return done

    def isAvailable(self, slot):
        """Returns True iff Split command is available"""
        if Configuration.get('SPLIT_BY_VALUE'):
            toTest = slot.handIsPairByValue
        else:
            toTest = slot.handIsPairByRank
        if not toTest:
            return False
        if not slot.playerCanAffordSplit:
            return False
        if not slot.firstAction:
            return False
        num_splits_allowed = Configuration.get('RESPLIT_UP_TO')
        if (num_splits_allowed != Configuration.UNRESTRICTED and
            slot.numSplits + 1 >= num_splits_allowed):
            return False
        if (slot.handWasSplit and slot.handIsAcePair and
            not Configuration.get('RESPLIT_ACES')):
            return False
        return True
    
    def __str__(self):
        """Returns string representing Split Command"""
        return 'Split'

    def __repr__(self):
        """Returns representation of Split Command"""
        return 'Sp'

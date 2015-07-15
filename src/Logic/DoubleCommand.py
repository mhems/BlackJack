####################
#
# DoubleCommand.py
#
####################

from src.Logic.Command import Command
from src.Utilities.Configuration import Configuration

class DoubleCommand(Command):
    """Representation of the double down action"""

    def __init__(self, hitCommand, standCommand):
        """Initialize members"""
        self.__hit_command   = hitCommand
        self.__stand_command = standCommand

    def perform(self, slot, **kwargs):
        """Perform Double command"""
        slot.doublePot()
        self.__hit_command.execute(slot, **kwargs)
        return self.__stand_command.execute(slot, **kwargs)

    def isAvailable(self, slot):
        """Double available depending on configuration"""
        if not slot.playerCanAffordDouble:
            return False
        if not slot.firstAction:
            return False
        double_range = Configuration.get('TOTALS_ALLOWED_FOR_DOUBLE')
        if (double_range != Configuration.UNRESTRICTED and
            not slot.handValue in double_range):
            return False
        if (slot.handWasSplit and
            not Configuration.get('DOUBLE_AFTER_SPLIT_ALLOWED')):
            return False
        return True
            
    def __str__(self):
        """Returns string representing Double Command"""
        return 'Double'

    def __repr__(self):
        """Returns representation of Double Command"""
        return 'D'

####################
#
# SurrenderCommand.py
#
####################

from src.Logic.Command import Command
from src.Utilities.Configuration import Configuration

class SurrenderCommand(Command):
    """Representation of the (late) surrender action"""

    def perform(self, slot, **kwargs):
        """Perform Surrender command"""
        slot.surrendered = True
        return True

    def isAvailable(self, slot):
        """Returns True iff (late) surrender is available"""
        return Configuration.get('LATE_SURRENDER') and slot.firstAction
    
    def __str__(self):
        """Returns string representing Surrender Command"""
        return 'Surrender'

    def __repr__(self):
        """Returns representation of Surrender Command"""
        return 'SU'
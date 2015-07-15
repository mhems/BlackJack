####################
#
# SurrenderCommand.py
#
####################

from src.Logic.Command import Command

class SurrenderCommand(Command):
    """Representation of the (late) surrender action"""

    def __perform(self, slot, **kwargs):
        """Perform Surrender command"""
        pass

    def isAvailable(self, slot):
        """Returns True iff (late) surrender is available"""
        pass
    
    def __str__(self):
        """Returns string representing Surrender Command"""
        return 'Surrender'

    def __repr__(self):
        """Returns representation of Surrender Command"""
        return 'SU'

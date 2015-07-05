####################
#
# EarlySurrenderCommand.py
#
####################

from src.Logic.Command import Command

class EarlySurrenderCommand(Command):
    """Representation of the early surrender action"""

    def __perform(self, slot, **kwargs):
        """Perform Early Surrender command"""
        pass

    def isAvailable(self, slot):
        """Return True iff early surrender is available"""
        pass
    
    def __str__(self):
        """Returns string representing Early Surrender Command"""
        return 'Early Surrender'

    def __repr__(self):
        """Returns representation of Early Surrender Command"""
        return 'ES'

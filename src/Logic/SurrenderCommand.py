####################
#
# SurrenderCommand.py
#
####################

class SurrenderCommand(Command):
    """Representation of the (late) surrender action"""

    def perform(self):
        """Perform Surrender command"""
        pass
        
    def __str__(self):
        """Returns string representing Surrender Command"""
        return 'Surrender'

    def __repr__(self):
        """Returns representation of Surrender Command"""
        return 'SU'

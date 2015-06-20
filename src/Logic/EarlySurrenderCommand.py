####################
#
# EarlySurrenderCommand.py
#
####################

class EarlySurrenderCommand(Command):
    """Representation of the early surrender action"""

    def perform(self):
        """Perform Early Surrender command"""
        pass
        
    def __str__(self):
        """Returns string representing Early Surrender Command"""
        return 'Early Surrender'

    def __repr__(self):
        """Returns representation of Early Surrender Command"""
        return 'ES'

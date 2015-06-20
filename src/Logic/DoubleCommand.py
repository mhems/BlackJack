####################
#
# DoubleCommand.py
#
####################

class DoubleCommand(Command):
    """Representation of the double down action"""

    def perform(self):
        """Perform Double command"""
        pass
        
    def __str__(self):
        """Returns string representing Double Command"""
        return 'Double'

    def __repr__(self):
        """Returns representation of Double Command"""
        return 'D'

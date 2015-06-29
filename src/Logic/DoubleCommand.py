####################
#
# DoubleCommand.py
#
####################

class DoubleCommand(Command):
    """Representation of the double down action"""

    def execute(self):
        """Perform Double command"""
        self.__player.double()
        
    def __str__(self):
        """Returns string representing Double Command"""
        return 'Double'

    def __repr__(self):
        """Returns representation of Double Command"""
        return 'D'

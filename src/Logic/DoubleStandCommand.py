####################
#
# DoubleStandCommand.py
#
####################

class DoubleStandCommand(Command):
    """Representation of the double down action, or stand if double not offered"""

    def execute(self):
        """Perform DoubleStand command"""
        self.__player.double_or_stand()
        
    def __str__(self):
        """Returns string representing Double or Stand Command"""
        return 'Double or Stand'

    def __repr__(self):
        """Returns representation of Double or Stand Command"""
        return 'Ds'

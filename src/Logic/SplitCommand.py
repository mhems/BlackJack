####################
#
# SplitCommand.py
#
####################

class SplitCommand(Command):
    """Representation of the split command"""

    def execute(self):
        """Perform Split command"""
        self.__player.split()
        
    def __str__(self):
        """Returns string representing Split Command"""
        return 'Split'

    def __repr__(self):
        """Returns representation of Split Command"""
        return 'Sp'

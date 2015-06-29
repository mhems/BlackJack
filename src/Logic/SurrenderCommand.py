####################
#
# SurrenderCommand.py
#
####################

class SurrenderCommand(Command):
    """Representation of the (late) surrender action"""

    def execute(self):
        """Perform Surrender command"""
        self.__player.surrender()
        
    def __str__(self):
        """Returns string representing Surrender Command"""
        return 'Surrender'

    def __repr__(self):
        """Returns representation of Surrender Command"""
        return 'SU'

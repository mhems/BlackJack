####################
#
# EarlySurrenderCommand.py
#
####################

class EarlySurrenderCommand(Command):
    """Representation of the early surrender action"""

    def execute(self):
        """Perform Early Surrender command"""
        self.__player.early_surrender()
        
    def __str__(self):
        """Returns string representing Early Surrender Command"""
        return 'Early Surrender'

    def __repr__(self):
        """Returns representation of Early Surrender Command"""
        return 'ES'

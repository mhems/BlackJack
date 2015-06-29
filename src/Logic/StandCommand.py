####################
#
# StandCommand.py
#
####################

class StandCommand(Command):
    """Representation of the stand (stay) action"""

    def execute(self):
        """Perform Stand command"""
        self.__player.stand()
        
    def __str__(self):
        """Returns string representing Stand Command"""
        return 'Stand'

    def __repr__(self):
        """Returns representation of Stand Command"""
        return 'S'

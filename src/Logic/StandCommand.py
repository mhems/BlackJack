####################
#
# StandCommand.py
#
####################

class StandCommand(Command):
    """Representation of the stand (stay) action"""

    def perform(self):
        """Perform Stand command"""
        pass
        
    def __str__(self):
        """Returns string representing Stand Command"""
        return 'Stand'

    def __repr__(self):
        """Returns representation of Stand Command"""
        return 'S'

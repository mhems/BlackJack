from src.Logic.Command import Command

class StandCommand(Command):
    """Representation of the stand (stay) action"""

    def perform(self, slot, **kwargs):
        """Perform Stand command"""
        return True

    def isAvailable(self, _):
        """Stand is always available"""
        return True

    def __str__(self):
        """Returns string representing Stand Command"""
        return 'Stand'

    def __repr__(self):
        """Returns representation of Stand Command"""
        return 'S'

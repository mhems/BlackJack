####################
#
# HitCommand.py
#
####################

class HitCommand(Command):
    """Representation of hit action"""

    def perform(self):
        """Perform Hit command"""
        pass
        
    def __str__(self):
        """Returns string representing Hit Command"""
        return 'Hit'

    def __repr__(self):
        """Returns representation of Hit Command"""
        return 'H'

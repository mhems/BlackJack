####################
#
# HitCommand.py
#
####################

class HitCommand(Command):
    """Representation of hit action"""

    def execute(self):
        """Perform Hit command"""
        self.__player.hit()
        
    def __str__(self):
        """Returns string representing Hit Command"""
        return 'Hit'

    def __repr__(self):
        """Returns representation of Hit Command"""
        return 'H'

####################
#
# DoubleHitCommand.py
#
####################

class DoubleHitCommand(Command):
    """Representation of the double down action, or hit if double not offered"""

    def execute(self):
        """Perform DoubleHit command"""
        self.__player.double_or_hit()
        
    def __str__(self):
        """Returns string representing Double or Hit Command"""
        return 'Double or Hit'

    def __repr__(self):
        """Returns representation of Double or Hit Command"""
        return 'Dh'

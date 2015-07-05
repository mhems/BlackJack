####################
#
# DoubleCommand.py
#
####################

from src.Logic.Command import Command

class DoubleCommand(Command):
    """Representation of the double down action"""

    def __init__(self, hitCommand, standCommand):
        """Initialize members"""
        self.__hit_command   = hitCommand
        self.__stand_command = standCommand

    def __perform(self, slot, **kwargs):
        """Perform Double command"""
        slot.doublePot()
        self.__hit_command.execute(slot, **kwargs)
        self.__stand_command.execute(slot, **kwargs)
        return False

    def isAvailable(self, slot):
        """Double available depending on configuration"""
        if not slot.playerCanDouble():
            return False
        if not slot.isFirstCommand():
            return False
        double_range = Configuration.get('CARDS_ALLOWED_FOR_DOUBLE')
        if not double_range == Configuration.RANGE_ALL:
            if not slot.handValue in double_range:
                return False
        if (slot.handWasSplit() and
            not Configuration.get('DOUBLE_AFTER_SPLIT_ALLOWED')):
            return False
        return True
            
    def __str__(self):
        """Returns string representing Double Command"""
        return 'Double'

    def __repr__(self):
        """Returns representation of Double Command"""
        return 'D'

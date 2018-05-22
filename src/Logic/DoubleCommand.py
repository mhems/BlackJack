from src.Logic.Command import Command
import src.Utilities.Configuration as config

class DoubleCommand(Command):
    """Representation of the double down action"""

    def __init__(self, hitCommand, standCommand):
        """Initialize members"""
        self.hit_command = hitCommand
        self.stand_command = standCommand

    def perform(self, slot, **kwargs):
        """Perform Double command"""
        slot.multiplyPot(config.get('DOUBLE_RATIO'))
        self.hit_command.execute(slot, **kwargs)
        return self.stand_command.execute(slot, **kwargs)

    def isAvailable(self, slot):
        """Double available depending on configuration"""
        if not slot.playerCanAffordDouble:
            return False
        if not slot.firstAction:
            return False
        double_range = config.get('TOTALS_ALLOWED_FOR_DOUBLE')
        if (double_range != config.UNRESTRICTED and
            not slot.hand.value in double_range):
            return False
        if (slot.hand.wasSplit and
            not config.get('DOUBLE_AFTER_SPLIT_ALLOWED')):
            return False
        return True

    def __str__(self):
        """Returns string representing Double Command"""
        return 'Double'

    def __repr__(self):
        """Returns representation of Double Command"""
        return 'D'

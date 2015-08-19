####################
#
# HitCommand.py
#
####################

from src.Logic.Command import Command

class HitCommand(Command):
    """Representation of hit action"""

    def __init__(self, shoe):
        """Initializes members"""
        self.__shoe = shoe

    def perform(self, slot, **kwargs):
        """Perform Hit command"""
        slot.addCards(self.__shoe.dealOneCard())
        return False

    def isAvailable(self, slot):
        """Returns True iff Hit command is available"""
        return True

    def __str__(self):
        """Returns string representing Hit Command"""
        return 'Hit'

    def __repr__(self):
        """Returns representation of Hit Command"""
        return 'H'

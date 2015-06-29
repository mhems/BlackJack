####################
#
# TableSlot.py
#
####################

class TableSlot:
    "Representation of one seat at the table (player, pot, hand)"""

    def __init__(self):
        self.__player = None
        self.__pot    = None
        self.__hand   = None

    def isActive(self):
        """Return True iff seated player has placed money to play"""
        return self.__pot > 0

    def isOccupied(self):
        """Return True iff slot has seated player"""
        return self.__player != None

    def promptAction(self, upcard):
        """Prompts player to act"""
        if self.isOccupied():
            return self.__player.act(self.__hand, upcard)
        else:
            

    def promptBet(self):
        """Prompts player to bet"""
        if self.isOccupied():
            self.__pot = self.__player.bet()

    def rakePot(self):
        """Rakes pot, setting it to zero"""
        amt = self.__pot
        self.__pot = 0
        return amt

    def 

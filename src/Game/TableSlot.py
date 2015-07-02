####################
#
# TableSlot.py
#
####################

class TableSlot:
    "Representation of one seat at the table (player, pot, hand)"""

    def __init__(self):
        self.__player = None
        self.__hand   = None
        self.__pot    = 0

    @property
    def player(self):
        return self.__player

    def isActive(self):
        """Return True iff seated player has placed money to play"""
        return self.__pot > 0

    def isOccupied(self):
        """Return True iff slot has seated player"""
        return self.__player != None

    def seatPlayer(self, player):
        """Seats player at table slot"""
        self.__player = player

    def unseatPlayer(self):
        """Removes player from table slot"""
        self.__player = None

    def addCard(self, card):
        """Adds card to hand"""
        self.__hand.addCards(card)

    def promptAction(self, upcard):
        """Prompts player to act"""
        # Need to have bet to act
        if self.isActive():
            return self.__player.act(self.__hand, upcard)

    def takeTurn(self, upcard):
        """Prompts player to act until 21, stand, or bust"""
        pass
        
    def promptBet(self):
        """Prompts player to bet"""
        # Need to have a player to bet
        if self.isOccupied():
            self.__pot = self.__player.bet()

    def rakePot(self):
        """Rakes pot, setting it to zero"""
        amt = self.__pot
        self.__pot = 0
        return amt

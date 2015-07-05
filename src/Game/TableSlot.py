####################
#
# TableSlot.py
#
####################

from src.Logic.Command import Command

class TableSlot:
    "Representation of one seat at the table (player, pot, hand)"""

    def __init__(self):
        self.__player    = None
        self.__hands     = []
        self.__pot       = 0
        self.__insurance = 0
        self.index       = 0

    @property
    def player(self):
        """Return player seated at slot"""
        return self.__player

    @property
    def hand(self):
        """Return current hand being acted upon"""
        return self.__hands[self.index]

    @property
    def handIsAcePair(self):
        """Return True iff hand is pair of Aces"""
        return self.hand.isPairByRank() and self.hand.hasAce()

    @property
    def numSplits(self):
        """Returns number of times player has split this round"""
        return len(self.__hands)

    @property
    def handWasSplit(self):
        """Returns True iff hand came from a split"""
        return self.hand.wasSplit

    @property
    def handIsAcePair(self):
        """Returns True iff hand is pair of Aces"""
        return self.hand.isAcePair
    
    def playerCanDoubleBet(self):
        """Return True iff player has adequate funds to double bet"""
        return player.stackAmount >= self.__pot

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
        self.hand.addCards(card)

    def promptAction(self, upcard):
        """Prompts player to act"""
        # Need to have bet to act
        if self.isActive():
            return self.__player.act(self.hand, upcard)

    def promptBet(self, **kwargs):
        """Prompts player to bet"""
        # Need to have a player to bet
        if self.isOccupied():
            self.__pot = self.__player.bet(**kwargs)

    def rakePot(self):
        """Rakes pot, setting it to zero"""
        amt = self.__pot
        self.__pot = 0
        return amt

    def hasBlackjack(self):
        """Returns True iff hand is natural blackjack"""
        return self.hand.isBlackjack()

    def doublePot(self):
        """Doubles player's pot"""
        pass

    def splitHand(self):
        """Splits player's hand into 2 new hands"""
        pass

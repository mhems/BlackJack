####################
#
# TableSlot.py
#
####################

from src.Basic.BlackjackHand import BlackjackHand

class TableSlot:
    "Representation of one seat at the table (player, pot, hand)"""

    def __init__(self):
        self.__player    = None
        self.__hands     = [BlackjackHand()]
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
    def handValue(self):
        """Return value of current hand"""
        return self.hand.value
    
    @property
    def hands(self):
        """Return all hands in play for slot"""
        return self.__hands
    
    @property
    def firstAction(self):
        """Return True iff player is on first action for hand"""
        return self.hand.numCards == 2
    
    @property
    def numSplits(self):
        """Returns number of times player has split this round"""
        return len(self.__hands) - 1

    @property
    def handWasSplit(self):
        """Returns True iff hand came from a split"""
        return self.hand.wasSplit

    @property
    def handIsAcePair(self):
        """Returns True iff hand is pair of Aces"""
        return self.hand.isAcePair
    
    @property
    def playerCanDoubleBet(self):
        """Return True iff player has adequate funds to double bet"""
        return self.player.stackAmount >= self.__pot

    @property
    def isActive(self):
        """Return True iff seated player has placed money to play"""
        return self.__pot > 0

    @property
    def isOccupied(self):
        """Return True iff slot has seated player"""
        return self.__player != None

    @property
    def hasBlackjack(self):
        """Returns True iff hand is natural blackjack"""
        return self.hand.isBlackjack
    
    def seatPlayer(self, player):
        """Seats player at table slot"""
        self.__player = player

    def unseatPlayer(self):
        """Removes player from table slot"""
        self.__player = None

    def addCards(self, *cards):
        """Adds card to hand"""
        self.hand.addCards(*cards)

    def beginRound(self):
        """Executes any actions necessary to begin turn"""
        self.__hands     = [BlackjackHand()]
        self.__pot       = 0
        self.__insurance = 0
        self.index       = 0
        
    def endRound(self):
        """Executes any actions necessary to end turn"""
        pass        
        
    def promptAction(self, upcard, availableCommands):
        """Prompts player to act"""
        return self.__player.act(self.hand, upcard, availableCommands)

    def promptBet(self, **kwargs):
        """Prompts player to bet"""
        self.__pot = self.__player.bet(**kwargs)

    def rakePot(self):
        """Rakes pot, setting it to zero"""
        amt = self.__pot
        self.__pot = 0
        return amt

    def doublePot(self):
        """Doubles player's pot"""
        self.__pot += player.wager(self.__pot)

    def splitHand(self):
        """Splits player's hand into 2 new hands"""
        (card1, card2) = self.hand.splitCards
        self.__hands[self.index] = BlackjackHand()
        self.__hands[self.index].addCards(card1)
        self.__hands[self.index].wasSplit = True
        self.__hands.insert(self.index + 1, BlackjackHand())
        self.__hands[self.index + 1].addCards(card2)
        self.__hands[self.index + 1].wasSplit = True

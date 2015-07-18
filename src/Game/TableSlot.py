####################
#
# TableSlot.py
#
####################

from src.Basic.BlackjackHand import BlackjackHand
from src.Utilities.Configuration import Configuration

class TableSlot:
    "Representation of one seat at the table (player, pot, hand)"""

    def __init__(self):
        self.__player    = None
        self.__hands     = [BlackjackHand()]
        # break to ensure correct usage
        self.__p       = 0
        self.__pots      = [0]
        self.__insurance = 0
        self.__insured   = False
        self.index       = 0
        self.surrendered = False

    @property
    def player(self):
        """Return player seated at slot"""
        return self.__player

    @property
    def hand(self):
        """Return current hand being acted upon"""
        return self.__hands[self.index]

    @property
    def pot(self):
        """Return amount of money in current pot"""
        return self.__pots[self.index]

    @property
    def insurance(self):
        """Return amount of insurance in side bet"""
        return self.__insurance
    
    @property
    def handValue(self):
        """Return value of current hand"""
        return self.hand.value
    
    @property
    def hands(self):
        """Return all hands in play for slot"""
        return self.__hands

    @property
    def pots(self):
        """Return all pots for slot"""
        return self.__pots
    
    @property
    def firstAction(self):
        """Return True iff player is on first action for hand"""
        return self.hand.numCards == 2
    
    @property
    def numSplits(self):
        """Returns number of times player has split this round"""
        return len(self.__hands) - 1

    @property
    def handIsBust(self):
        """Return True iff hand is bust"""
        return self.hand.isBust

    @property
    def handWasSplit(self):
        """Returns True iff hand came from a split"""
        return self.hand.wasSplit

    @property
    def handIsAcePair(self):
        """Returns True iff hand is pair of Aces"""
        return self.hand.isAcePair

    @property
    def handIsPairByValue(self):
        """Returns True iff hand is pair by value"""
        return self.hand.isPairByValue

    @property
    def handIsPairByRank(self):
        """Returns True iff hand is pair by rank"""
        return self.hand.isPairByRank
    
    @property
    def playerCanAffordDouble(self):
        """Return True iff player has adequate funds to double"""
        print('afford double', self.index)
        return (self.player.stackAmount >=
                Configuration.get('DOUBLE_RATIO') * self.pot)

    @property
    def playerCanAffordSplit(self):
        """Return True iff player has adequate funds to split"""
        print('afford split', self.index)
        return (self.player.stackAmount >=
                Configuration.get('SPLIT_RATIO') * self.pot)

    @property
    def playerCanAffordInsurance(self):
        """Return True iff player has adequate funds to insurance"""
        return (self.player.stackAmount >=
                Configuration.get('INSURANCE_RATIO') * self.pot)
    
    @property
    def isActive(self):
        """Return True iff seated player has placed money to play"""
        return self.pot > 0

    @property
    def isOccupied(self):
        """Return True iff slot has seated player"""
        return self.__player != None

    @property
    def insured(self):
        """Return True iff player is insured"""
        return self.__insured
    
    @property
    def hasNaturalBlackjack(self):
        """Returns True iff hand is natural blackjack"""
        return self.hand.isNaturalBlackjack

    @property
    def handIsBlackjackValued(self):
        """Returns True iff hand is blackjack valued"""
        return self.hand.isBlackjackValued

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
        self.__pots      = [0]
        self.__insurance = 0
        self.index       = 0
        
    def endRound(self):
        """Executes any actions necessary to end turn"""
        pass

    def promptAction(self, upcard, availableCommands, **kwargs):
        """Prompts player to act"""
        return self.__player.act(self.hand, upcard, availableCommands, **kwargs)

    def promptInsurance(self, **kwargs):
        """Prompts player for insurance"""
        if self.playerCanAffordInsurance and self.__player.insure(self.hand, **kwargs):
            self.__insured = True
            self.__insurance = self.__player.wager(
                self.pot * Configuration.get('INSURANCE_RATIO'))
            
    def promptBet(self, **kwargs):
        """Prompts player to bet"""
        self.__pots[self.index] = self.__player.bet(**kwargs)

    def promptEarlySurrender(self, upcard, **kwargs):
        """Prompts player for early surrender"""
        if self.__player.earlySurrender(self.hand, upcard, **kwargs):
            pass

    def promptLateSurrender(self, upcard, **kwargs):
        """Prompts player for late surrender"""
        if self.__player.lateSurrender(self.hand, upcard, **kwargs):
            pass
        
    def rakePot(self, fraction=1):
        """Rakes and returns specified fraction of pot"""
        amt = self.pot * fraction
        self.__pots[self.index] -= amt
        print('raking', amt)
        return amt

    def rakeInsurance(self):
        """Rakes and empties insurance"""
        amt = self.__insurance
        self.__insurance = 0
        return amt

    def payout(self, amt):
        """Pays seated player amt"""
        print('receiving', amt)
        self.__player.receive_payment(amt)
    
    def multiplyPot(self, factor):
        """Adds factor of current pot to pot"""
        print('before')
        print(self.pot, self.__player.stackAmount)
        self.__pots[self.index] += self.__player.wager(self.pot * factor)
        print('after')
        print(self.pot, self.__player.stackAmount)
        
    def splitHand(self):
        """Splits player's hand into 2 new hands"""
        (card1, card2) = self.hand.splitCards
        self.__hands[self.index] = BlackjackHand()
        self.__hands[self.index].addCards(card1)
        self.__hands[self.index].wasSplit = True
        self.__hands.insert(self.index + 1, BlackjackHand())
        self.__pots.insert(self.index + 1,
                           (self.__pots[self.index] *
                            Configuration.get('SPLIT_RATIO') ) )
        self.__hands[self.index + 1].addCards(card2)
        self.__hands[self.index + 1].wasSplit = True

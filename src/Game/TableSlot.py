from math import floor

from src.Basic.BlackjackHand import BlackjackHand
import src.Utilities.Configuration as config

class TableSlot:
    """Representation of one seat at the table (player, pot, hand)"""

    def __init__(self):
        self.player = None
        self.hands = [BlackjackHand()]
        self.pots = [0]
        self.insurance = 0
        self.insured = False
        self.index = 0
        self.surrendered = False
        self.settled = False

    @property
    def hand(self):
        """Return current hand being acted upon"""
        return self.hands[self.index]

    @property
    def pot(self):
        """Return amount of money in current pot"""
        return self.pots[self.index]

    @property
    def firstAction(self):
        """Return True iff player is on first action for hand"""
        return self.hand.numCards == 2

    @property
    def numSplits(self):
        """Returns number of times player has split this round"""
        return len(self.hands) - 1

    @property
    def playerCanAffordDouble(self):
        """Return True iff player has adequate funds to double"""
        return self._canAfford('DOUBLE_RATIO')

    @property
    def playerCanAffordSplit(self):
        """Return True iff player has adequate funds to split"""
        return self._canAfford('SPLIT_RATIO')

    @property
    def playerCanAffordInsurance(self):
        """Return True iff player has adequate funds to insurance"""
        return self._canAfford('INSURANCE_RAIO')

    @property
    def isActive(self):
        """Return True iff seated player has placed money to play"""
        return self.pots[0] > 0

    @property
    def isOccupied(self):
        """Return True iff slot has seated player"""
        return self.player != None

    def seatPlayer(self, player):
        """Seats player at table slot"""
        self.player = player

    def unseatPlayer(self):
        """Removes player from table slot"""
        self.player = None

    def addCards(self, *cards):
        """Adds card to hand"""
        self.hand.addCards(*cards)

    def beginRound(self):
        """Executes any actions necessary to begin turn"""
        self.promptBet()

    def endRound(self):
        """Executes any actions necessary to end turn"""
        if self.isOccupied:
            self.player.receive_payment(sum(self.pots))
            self.player.receive_payment(self.insurance)
        self.pots = [0]
        self.insurance = 0
        self.insured = False
        self.index = 0
        self.settled = False
        self.surrendered = False
        self.clearHands()

    def clearHands(self):
        """Resets any hands in slot"""
        self.hands = [self.hands[0]]
        self.hands[0].reset()

    def promptAction(self, upcard, availableCommands, **kwargs):
        """Prompts player to act"""
        return self.player.act(self.hand, upcard, availableCommands, **kwargs)

    def promptInsurance(self, **kwargs):
        """Prompts player for insurance"""
        if ( self.playerCanAffordInsurance and
             self.player.insure(self.hand,**kwargs) ):
            self.insured = True
            self.insurance = self.player.wager(
                self.pots[0] * config.get('INSURANCE_RATIO'))

    def promptBet(self, **kwargs):
        """Prompts player to bet"""
        amt = self.player.amountToBet(**kwargs)
        if amt >= self.pot:
            self.pots[self.index] += self.player.wager(amt - self.pot)
        else:
            self.player.receive_payment(self.pot - amt)

    def promptEarlySurrender(self, upcard, **kwargs):
        """Prompts player for early surrender"""
        if self.player.earlySurrender(self.hand, upcard, **kwargs):
            pass

    def takePot(self, fraction=1):
        """Takes and returns specified fraction of pot"""
        amt = floor(self.pot * fraction)
        self.pots[self.index] -= amt
        return amt

    def takeInsurance(self):
        """Takes and empties insurance"""
        amt = self.insurance
        self.insurance = 0
        return amt

    def payToPot(self, amt):
        """Places amt in pot"""
        self.pots[self.index] += amt

    def splitHand(self):
        """Splits player's hand into 2 new hands with one card each"""
        (card1, card2) = self.hand.splitCards
        self.hands[self.index] = BlackjackHand()
        self.hands[self.index].addCards(card1)
        self.hands[self.index].wasSplit = True
        self.hands.insert(self.index + 1, BlackjackHand())
        split_bet = floor( self.pots[self.index] *
                           config.get('SPLIT_RATIO') )
        self.player.wager(split_bet)
        self.pots.insert(self.index + 1, split_bet)
        self.hands[self.index + 1].addCards(card2)
        self.hands[self.index + 1].wasSplit = True

    def _canAfford(self, ratioName):
        needed_amt = floor(self.pot * config.get(ratioName))
        return self.player.stack.amount >= needed_amt

####################
#
# BlackjackHand.py
#
####################

from itertools import groupby

from src.Basic.Card import Card
from src.Basic.Hand import Hand
from src.Utilities.Configuration import Configuration

class BlackjackHand(Hand):
    """Represents Blackjack hand"""

    def __init__(self):
        """Initializes hand to have no cards"""
        self.__cards = []
        self.wasSplit = False

    @property
    def value(self):
        """Returns largest non-bust value if possible, else largest value"""
        val = sum([c.value for c in self.__cards if not c.isAce])
        nAces = self.numAces
        if nAces > 0:
            val += (nAces - 1) * Card.SOFT_ACE_VALUE
            if val + Card.HARD_ACE_VALUE <= Configuration.get('BLACKJACK_VALUE'):
                val += Card.HARD_ACE_VALUE
            else:
                val += Card.SOFT_ACE_VALUE
        return val

    @property
    def ranks(self):
        """Returns list of ranks in hand"""
        return [c.rank for c in self.__cards]

    @property
    def isAcePair(self):
        """Return True iff hand is pair of Aces"""
        return self.numAces == 2 and self.numCards == 2

    @property
    def isSoft17(self):
        """Return True iff hand is soft 17"""
        return self.value == 17 and self.isSoft

    @property
    def isSoft(self):
        """Return True iff hand is soft (i.e. contains hard-valued ace)"""
        val = sum((c.value for c in self.__cards if not c.isAce))
        numAces = self.numAces
        if numAces > 0:
            val += (numAces - 1) * Card.SOFT_ACE_VALUE
            if val + Card.HARD_ACE_VALUE <= Configuration.get('BLACKJACK_VALUE'):
                return True
        return False

    @property
    def numCards(self):
        """Returns number of cards in hand"""
        return len(self.__cards)

    @property
    def numAces(self):
        """Returns number of ace cards in hand"""
        return len([c for c in self.__cards if c.isAce])

    @property
    def isBlackjackValued(self):
        """Returns True iff hand has value equal to Blackjack value"""
        return self.value == Configuration.get('BLACKJACK_VALUE')

    @property
    def isNaturalBlackjack(self):
        """Returns True iff hand is natural blackjack"""
        """Note a blackjack after split is NOT considered natural"""
        return (self.numCards == 2 and
                self.value == Configuration.get('BLACKJACK_VALUE') and
                not self.wasSplit)

    @property
    def isPairByRank(self):
        """Returns True iff initial two cards are equal in rank"""
        return (self.numCards == 2 and
                self.__cards[0].rankEquivalent(self.__cards[1]))

    @property
    def isPairByValue(self):
        """Returns True iff initial two cards are equal in value"""
        return (self.numCards == 2 and
                self.__cards[0].valueEquivalent(self.__cards[1]))

    @property
    def isBust(self):
        """Returns True iff hand value is greater than blackjack value"""
        return self.value > Configuration.get('BLACKJACK_VALUE')

    @property
    def hasAce(self):
        """Returns True iff hand has at least one ace"""
        return self.numAces >= 1

    @property
    def splitCards(self):
        """Returns cards as tuple"""
        if self.numCards > 2:
            raise Exception('Cannot split hand of more than 2 cards')
        return tuple(self.__cards)

    def addCards(self, *cards):
        """Adds args to hand"""
        self.__cards.extend(cards)

    def reset(self):
        """Removes all cards from hand"""
        self.__cards = []

    def __eq__(self, other):
        """Returns True iff cards in self are same as in other"""
        if self.numCards != other.numCards:
            return False
        for c1 in self.__cards:
            if not c1 in other.__cards:
                return False
        return True

    def __str__(self):
        """Returns comma delimited list of cards' representations"""
        return '[' + ', '.join((str(c) for c in self.__cards)) +']'

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
    def isBlackjack(self):
        """Returns True iff initial two cards sum to blackjack value"""
        return (self.numCards == 2 and
                self.value == Configuration.get('BLACKJACK_VALUE'))
    
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

    def addCards(self, *cards):
        """Adds args to hand"""
        self.__cards.extend(cards)

    def reset(self):
        """Removes all cards from hand"""
        self.__cards = []
            
    def __str__(self):
        """Returns comma delimited list of cards' representations"""
        return '[' + ', '.join((str(c) for c in self.__cards)) +']'

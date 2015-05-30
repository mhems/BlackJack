####################
#
# BlackjackHand.py
#
####################

from itertools import groupby
from src.Basic.Card import *
from . import Hand

class BlackjackHand(Hand.Hand):
    """Represents Blackjack hand"""
    
    BLACKJACK_VALUE = 21
    
    def __init__(self):
        """Initializes hand to have no cards"""
        self.__cards = []

    def value(self):
        """Returns largest non-bust value if possible, else largest value"""
        val = sum([c.value for c in self.__cards if not c.isAce()])
        nAces = self.numAces()
        if nAces > 0:
            if nAces > 1:
                val += (nAces - 1) * Card.SOFT_ACE_VALUE
            if val + Card.HARD_ACE_VALUE <= BlackjackHand.BLACKJACK_VALUE:
                val += Card.HARD_ACE_VALUE
            else:
                val += Card.SOFT_ACE_VALUE
        return val
    
    def numCards(self):
        """Returns number of cards in hand"""
        return len(self.__cards)

    def numAces(self):
        """Returns number of ace cards in hand"""
        return len([c for c in self.__cards if c.isAce()])

    def isBlackjack(self):
        """Returns True iff initial two cards sum to blackjack value"""
        return self.numCards() == 2 and self.value() == BlackjackHand.BLACKJACK_VALUE
    
    def isPairByRank(self):
        """Returns True iff initial two cards are equal in rank"""
        return self.numCards() == 2 and self.__cards[0].rankEquivalent(self.__cards[1])

    def isPairByValue(self):
        """Returns True iff initial two cards are equal in value"""
        return self.numCards() == 2 and self.__cards[0].valueEquivalent(self.__cards[1])
    
    def isBust(self):
        """Returns True iff no hand variant is less than or equal to blackjack value"""
        return self.value() > BlackjackHand.BLACKJACK_VALUE

    def hasAce(self):
        """Returns True iff hand has at least one ace"""
        return self.numAces() >= 1

    def addCards(self,cards):
        """Adds args to hand"""
        self.__cards.extend(cards)

    def reset(self):
        """Removes all cards from hand"""
        self.__cards = []
            
    def __str__(self):
        """Returns comma delimited list of cards' representations"""
        return '[' + ', '.join((str(c) for c in self.__cards)) +']'

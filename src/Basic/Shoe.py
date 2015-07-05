####################
#
# Shoe.py
#
####################
from math import floor

from src.Basic.Card import Card
from src.Utilities.Configuration import Configuration

class Shoe:
    """Represents a shoe of decks for dealing purposes"""

    def __init__(self,n,algorithm,cutIndex=0):
        """Initializes shoe to have n decks, algorithm function for shuffling, and cutIndex"""
        self.__cards = []
        self.numDecks = n
        self.__algorithm = algorithm
        self.__index = 0
        if isinstance(cutIndex,float):
            self.cutIndex = int(floor(n * Card.NUM_CARDS_PER_DECK * cutIndex))
        else:
            self.cutIndex = cutIndex if cutIndex > 0 else n * Card.NUM_CARDS_PER_DECK - Card.NUM_CARDS_PER_DECK/2
        for _ in range(n):
            self.__cards.extend(Card.makeDeck())

    @property
    def numCardsRemainingToBeDealt(self):
        """Returns number of cards remaining to be dealt from shoe"""
        return self.cutIndex - self.__index

    @property
    def numCardsRemainingInShoe(self):
        """Returns number of cards remaining in shoe"""
        return self.numDecks * Card.NUM_CARDS_PER_DECK - self.__index
    
    @property
    def isExhausted(self):
        """Returns True iff all cards that will be dealt have been dealt"""
        return self.__index >= self.cutIndex

    @property
    def isEmpty(self):
        """Returns True iff all cards in shoe have been dealt"""
        """This is only possible if cut index == len(self.__cards)"""
        return self.__index >= self.numDecks * Card.NUM_CARDS_PER_DECK

    def deal(self,n=1):
        """Remove and return n cards from beginning of shoe"""
        c = []
        for i in range(n):
            c.append(self.dealOneCard())
        return c
    
    def dealOneCard(self):
        """Convenience method to deal one card"""
        if self.isExhausted:
            self.__cards = self.__algorithm(self.__cards)
            self.__index = 0
            self.deal(Configuration.get('NUM_CARDS_BURN_ON_SHUFFLE'))
        c = self.__cards[self.__index]
        self.__index += 1
        return c

def faro_shuffle(deck):
    N = len(deck)
    ret = []
    for (a,b) in zip(deck[:N], deck[N:]):
        ret.extend( (a, b) )
    return ret

def fisher_yates_shuffle(deck):
    for i in range(len(deck), 1, -1):
        j = randint(0, i)
        temp    = deck[i]
        deck[i] = deck[j]
        deck[j] = temp
    return deck

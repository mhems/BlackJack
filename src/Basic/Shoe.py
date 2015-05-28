####################
#
# Shoe.py
#
####################

from Card import *

class Shoe:
    """Represents a shoe of decks for dealing purposes"""

    NUM_CARDS_PER_DECK = 52

    def __init__(self,n,algorithm,cutIndex=0):
        """Initializes shoe to have n decks, algorithm function for shuffling, and cutIndex"""
        self.__cards = []
        self.numDecks = n
        self.__algorithm = algorithm
        self.__index = 0
        if isinstance(self.cutIndex,float):
            self.cutIndex = math.floor(n*Shoe.NUM_CARDS_PER_DECK*cutIndex)
        else:
            self.cutIndex = cutIndex if cutIndex > 0 else n * Shoe.NUM_CARDS_PER_DECK - Shoe.NUM_CARDS_PER_DECK/2
        for i in range(n):
            self.__decks.append(Card.makeDeck())

    def deal(self,n=1):
        """Remove and return n cards from beginning of shoe"""
        c = []
        for i in range(n):
            c.append(self.__dealOneCard())
        return c
    
    def __dealOneCard(self):
        """Convenience method to deal one card"""
        if self.isEmpty():
            self.__decks = self.__algorithm(self.__decks)
            self.__index = 0
            self.burn()
        c = self.__cards[self.__index]
        self.__index += 1
        return c
    
    def numCardsRemainingToBeDealt(self):
        """Returns number of cards remaining to be dealt from shoe"""
        return self.numDecks * Shoe.NUM_CARDS_PER_DECK - self.cutIndex

    def numCardsRemainingInShoe(self):
        """Returns number of cards remaining in shoe"""
        return self.numDecks * Shoe.NUM_CARDS_PER_DECK - self.__index
    
    def isExhausted(self):
        """Returns True iff all cards that will be dealt have been dealt"""
        return self.index >= self.cutIndex

    def isEmpty(self):
        """Returns True iff all cards in shoe have been dealt"""
        return self.index >= self.numDecks * Shoe.NUM_CARDS_PER_DECK

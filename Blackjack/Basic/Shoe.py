####################
#
# Shoe.py
#
####################

from Card import *

class Shoe:
    NUM_CARDS_PER_DECK = 52

    def __init__(self,n,algorithm,cutIndex=0):
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
        c = []
        for i in range(n):
            c.append(self.__dealOneCard())
        return c

    def burn(self,n=1):
        deal(n)

    def __dealOneCard(self):
        if self.isEmpty():
            self.__decks = self.__algorithm(self.__decks)
            self.__index = 0
            self.burn()
        c = self.__cards[self.__index]
        self.__index += 1
        return c
    
    def numCardsRemainingToBeDealt(self):
        return self.numDecks * Shoe.NUM_CARDS_PER_DECK - self.cutIndex

    def numCardsRemainingInShoe(self):
        return self.numDecks * Shoe.NUM_CARDS_PER_DECK - self.__index
    
    def isExhausted(self):
        return self.index >= self.cutIndex

    def isEmpty(self):
        return self.index >= self.numDecks * Shoe.NUM_CARDS_PER_DECK

if __name__ == '__main__':
    s = Shoe(6,None)
    print(s)

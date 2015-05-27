####################
#
# Shoe.py
#
####################

from Deck import *

class Shoe:

    def __init__(self, algorithm, n=6, end=7/8):
        self.decks = []
        self.numDecks = n
        self.index = 0
        self.algorithm = algorithm
        self.end = n * 52 * end
        for i in range(n):
            self.decks.append(Deck.makeDeck())

    def deal(self,n=1):
        t = []
        for i in range(n):
            t.append(self.__dealOneCard())
        return t

    def __dealOneCard(self):
        if self.isEmpty():
            self.shuffle()
        c = self.cards[self.index]
        self.index += 1
        return c
    
    def numCardsRemaining(self):
        return self.numDecks * 52 - self.index
    
    def isEmpty(self):
        return self.index >= self.numDecks * 52

    def reset(self):
        self.index = 0

    def shuffle(self):
        self.reset()
        algorithm.shuffle(self.cards)

    def __repr__(self):
        return "%d out of %d" % (self.index, self.numDecks)

    def __str__(self):
        return "On card # %d out of %d (%d decks)" % (self.index, self.numDecks*52, self.numDecks)

if __name__ == '__main__':
    s = Shoe(algorithm=None)
    print(s)

####################
#
# Deck.py
#
####################

from Card import *

class Deck:

    def __init__(self, algorithm):
        self.cards = Deck.makeDeck()
        self.index = 0
        self.algorithm = algorithm

    @staticmethod
    def makeDeck():
        cards = []
        for suit in Card.suits:
            for rank in Card.ranks:
                cards.append(Card(rank,suit))
        return cards

    def deal(self, n=1):
        if self.index + n > 52:
            self.shuffle()
        t = self.cards[self.index:self.index+n+1]
        self.index += n
        return t

    def numCardsRemaining(self):
        return 52 - self.index
    
    def isEmpty(self):
        return self.index >= 52

    def reset(self):
        self.index = 0

    def shuffle(self):
        self.reset()
        algorithm.shuffle(self.cards)
        
    def __repr__(self):
        return self.__asList()

    def __str__(self):
        return self.__asList('\n')

    def __asList(self, delim=','):
        s = delim.join((str(c) for c in self.cards[:self.index]))
        s += '>'
        s += delim
        s += delim.join((str(c) for c in self.cards[self.index:]))
        return s
    

if __name__ == '__main__':
    d = Deck(algorithm=None)
    print(d)

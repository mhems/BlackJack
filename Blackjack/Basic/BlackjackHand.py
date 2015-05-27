####################
#
# BlackjackHand.py
#
####################

from Card import *

class BlackjackHand:

    BLACKJACK_VALUE = 21
    
    def __init__(self):
        self.cards = []

    @property
    def value(self):
        pass

    @property
    def softValue(self):
        pass
    
    @property
    def numCards(self):
        return len(self.cards)

    def isBlackjack(self):
        return self.numCards == 2 and self.value == BlackjackHand.BLACKJACK_VALUE
    
    def isPair(self):
        return self.numCards == 2 and self.cards[0].rank == self.cards[1].rank

    def isBust(self):
        return self.value > BlackjackHand.BLACKJACK_VALUE

    def hasAce(self):
        return len(ifilter(lambda x: x.isAce(), self.cards)) >= 1

    def addCards(self,*args):
        if args:
            self.cards.extend(list(args))

    def reset(self):
        self.cards = []
            
    def __str__(self):
        return ', '.join((str(c) for c in self.cards))

            
if __name__ == '__main__':
    hand = BlackjackHand()
    hand.addCards(Card('A','C'),Card(4,'D'))
    print(hand)

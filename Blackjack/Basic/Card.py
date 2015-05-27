####################
#
# Card.py
#
####################

class Card:

    ranks = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
    suits = ['S','H','D','C']

    __charToNameDict = {}
    for i in range(2,11):
        __charToNameDict[i] = i
    __charToNameDict['J'] = 'Jack'
    __charToNameDict['Q'] = 'Queen'
    __charToNameDict['K'] = 'King'
    __charToNameDict['A'] = 'Ace'
    __charToNameDict['S'] = 'Spades'
    __charToNameDict['H'] = 'Hearts'
    __charToNameDict['D'] = 'Diamonds'
    __charToNameDict['C'] = 'Clubs'
    
    def __init__(self, rank, suit):
        self.__rank = rank if isinstance(rank,int) else rank[0].upper()
        self.__suit = suit[0].upper()
        if self.__rank not in Card.ranks:
            raise TypeError("Rank must be a number 2-10 or J, Q, K, A (Jack, Queen, King, or Ace)")
        if self.__suit not in Card.suits:
            raise TypeError("Suit must be one of S, H, D, C (Spades, Hearts, Diamonds, Clubs)")
        
    @property
    def rank(self):
        return Card.__charToNameDict[self.__rank]

    @rank.setter
    def rank(self,_):
        raise TypeError("Cannot set card's rank")

    @property
    def suit(self):
        return Card.__charToNameDict[self.__suit]
    
    @suit.setter
    def suit(self,_):
        raise TypeError("Cannot set card's suit")

    @property
    def value(self):
        if self.isAce():
            return [1,11]
        elif self.isFaceCard():
            return 10
        else:
            return self.rank

    @value.setter
    def value(self,_):
        raise TypeError("Cannot set card's value")

    def __str__(self):
        return str(self.rank) + ' of ' + self.suit

    def __repr__(self):
        return str(self.rank) + ' of ' + self.suit

    def isAce(self):
        return self.__rank == 'A'

    def isFaceCard(self):
        return self.__rank in ['J','Q','K','A']

    @staticmethod
    def makeDeck():
        cards = []
        for suit in Card.suits:
            for rank in Card.ranks:
                cards.append(Card(rank,suit))
        return cards

    
if __name__ == '__main__':
    c = Card(4,'D')
    print(c)
    #d = Card(4,'E')
    print(c.rank)
    print(c.suit)
    print(c.value)
    a = Card('A', 'D')
    print(a.value)
    j = Card('J', 'D')
    print(j.value)
    #    c.rank = 4

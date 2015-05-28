####################
#
# Card.py
#
####################

class Card:
    """Represents a playing card"""
    
    HARD_ACE_VALUE = 11
    SOFT_ACE_VALUE = 1
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
        """Initializes card's rank and suit to rank and suit respectively"""
        self.__rank = rank if isinstance(rank,int) else rank[0].upper()
        self.__suit = suit[0].upper()
        if self.__rank not in Card.ranks:
            raise TypeError("Rank must be a number 2-10 or J, Q, K, A (Jack, Queen, King, or Ace)")
        if self.__suit not in Card.suits:
            raise TypeError("Suit must be one of S, H, D, C (Spades, Hearts, Diamonds, Clubs)")
        
    @property
    def rank(self):
        """Returns rank of card"""
        return Card.__charToNameDict[self.__rank]

    @rank.setter
    def rank(self,_):
        """Prevents rank from being set"""
        raise TypeError("Cannot set card's rank")

    @property
    def suit(self):
        """Returns suit of card"""
        return Card.__charToNameDict[self.__suit]
    
    @suit.setter
    def suit(self,_):
        """Prevents suit from being set"""
        raise TypeError("Cannot set card's suit")

    @property
    def value(self):
        """Returns integer value of card"""
        if self.isAce():
            return Card.HARD_ACE_VALUE
        elif self.isFaceCard():
            return 10
        else:
            return self.rank

    @value.setter
    def value(self,_):
        """Prevents value from being set"""
        raise TypeError("Cannot set card's value")

    def __str__(self):
        """Returns canonical representation of card"""
        return str(self.rank) + ' of ' + self.suit

    def __repr__(self):
        """Returns canonical representation of card"""
        return str(self.rank) + ' of ' + self.suit

    def isAce(self):
        """Returns True iff card is an Ace"""
        return self.__rank == 'A'

    def isFaceCard(self):
        """Returns True iff card is a face card"""
        return self.__rank in ['J','Q','K','A']

    @staticmethod
    def makeDeck():
        """Returns list of 52 cards over all ranks and suits"""
        cards = []
        for suit in Card.suits:
            for rank in Card.ranks:
                cards.append(Card(rank,suit))
        return cards

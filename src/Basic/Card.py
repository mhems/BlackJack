####################
#
# Card.py
#
####################

class Card:
    """Represents a playing card"""
    
    HARD_ACE_VALUE = 11
    SOFT_ACE_VALUE = 1
    RANK_REGEX = '10|J(?:ack)?|Q(?:ueen)?|K(?:ing)?|A(?:ce)?|[2-9]'
    ranks  = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
    suits  = ['S','H','D','C']
    values = [2,3,4,5,6,7,8,9,10,'A']
    NUM_CARDS_PER_DECK = len(ranks) * len(suits)
    
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
    
    @staticmethod
    def makeDeck():
        """Returns list of 52 cards over all ranks and suits"""
        return [Card(r,s) for r in Card.ranks for s in Card.suits]

    def __init__(self, rank, suit):
        """Initializes card's rank and suit to rank and suit respectively"""
        self.__rank = rank if isinstance(rank,int) else rank[0].upper()
        self.__suit = suit[0].upper()
        if self.__rank not in Card.ranks:
            raise TypeError(
                'Rank must be a number 2-10 or J, Q, K, A'
                ' (Jack, Queen, King, or Ace)')
        if self.__suit not in Card.suits:
            raise TypeError(
                'Suit must be one of S, H, D, C'
                ' (Spades, Hearts, Diamonds, Clubs)')
        
    @property
    def rank(self):
        """Returns rank of card"""
        return Card.__charToNameDict[self.__rank]

    @property
    def suit(self):
        """Returns suit of card"""
        return Card.__charToNameDict[self.__suit]
    
    @property
    def value(self):
        """Returns integer value of card"""
        if self.isAce:
            return Card.HARD_ACE_VALUE
        elif self.isFaceCard:
            return 10
        else:
            return self.rank

    @property
    def isAce(self):
        """Returns True iff card is an Ace"""
        return self.__rank == 'A'

    @property
    def isFaceCard(self):
        """Returns True iff card is a face card"""
        return self.__rank in ['J','Q','K','A']
    
    def rankEquivalent(self, other):
        """Returns True iff other has equivalent rank"""
        return self.rank == other.rank

    def valueEquivalent(self, other):
        """Returns True iff other has equivalent value"""
        return self.value == other.value
    
    def __str__(self):
        """Returns canonical representation of card"""
        return str(self.rank) + ' of ' + self.suit

    def __repr__(self):
        """Returns canonical representation of card"""
        return str(self.rank) + ' of ' + self.suit

    def __eq__(self, other):
        """Returns True if self has equal rank and suit to that of other"""
        return self.__rank == other.__rank and self.__suit == other.__suit

    def __ne__(self, other):
        """Returns True iff self is not equal to other"""
        return not self == other

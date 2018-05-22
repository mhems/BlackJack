class Card:
    """Represents a playing card"""

    HARD_ACE_VALUE = 11
    SOFT_ACE_VALUE = 1
    RANK_REGEX = '10|J(?:ack)?|Q(?:ueen)?|K(?:ing)?|A(?:ce)?|[2-9]'
    ranks  = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
    suits  = ['S','H','D','C']
    values = [2,3,4,5,6,7,8,9,10,'A']
    NUM_CARDS_PER_DECK = len(ranks) * len(suits)

    charToNameDict = {}
    for i in range(2,11):
        charToNameDict[i] = str(i)
    charToNameDict['J'] = 'Jack'
    charToNameDict['Q'] = 'Queen'
    charToNameDict['K'] = 'King'
    charToNameDict['A'] = 'Ace'
    charToNameDict['S'] = 'Spades'
    charToNameDict['H'] = 'Hearts'
    charToNameDict['D'] = 'Diamonds'
    charToNameDict['C'] = 'Clubs'
    suits_strs = {
        'S' : '♠',
        'H' : '♥',
        'D' : '♦',
        'C' : '♣'
    }

    @staticmethod
    def makeDeck():
        """Returns list of 52 cards over all ranks and suits"""
        return [Card(r,s) for r in Card.ranks for s in Card.suits]

    def __init__(self, rank, suit):
        """Initializes card's rank and suit to rank and suit respectively"""
        self.rank = rank if isinstance(rank, int) else rank[0].upper()
        self.suit = suit[0].upper()
        if self.rank not in Card.ranks:
            raise TypeError('Rank must be a number 2-10 or J, Q, K, A')
        if self.suit not in Card.suits:
            raise TypeError('Suit must be one of S, H, D, C')

    @property
    def rankName(self):
        """Returns rank of card"""
        return Card.charToNameDict[self.rank]

    @property
    def suitName(self):
        """Returns suit of card"""
        return Card.charToNameDict[self.suit]

    @property
    def value(self):
        """Returns integer value of card"""
        if self.isAce:
            return Card.HARD_ACE_VALUE
        elif self.isFaceCard:
            return 10
        return self.rank

    @property
    def isAce(self):
        """Returns True iff card is an Ace"""
        return self.rank == 'A'

    @property
    def isFaceCard(self):
        """Returns True iff card is a face card"""
        return self.rank in ('J','Q','K','A')

    def rankEquivalent(self, other):
        """Returns True iff other has equivalent rank"""
        return self.rank == other.rank

    def valueEquivalent(self, other):
        """Returns True iff other has equivalent value"""
        return self.value == other.value

    def __str__(self):
        """Returns canonical representation of card"""
        return self.rankName + ' of ' + self.suitName

    def __repr__(self):
        """Returns canonical representation of card"""
        return self.__str__()

    def __eq__(self, other):
        """Returns True if self has equal rank and suit to that of other"""
        return self.rank == other.rank and self.suit == other.suit

    def __ne__(self, other):
        """Returns True iff self is not equal to other"""
        return not self == other

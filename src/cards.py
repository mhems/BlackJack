from abc import ABCMeta, abstractmethod
from math import floor
from random import Random

from config import get

class Card:
    """Represents a playing card"""

    ranks  = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
    suits  = ['S','H','D','C']

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
        self.index = Card.ranks.index(self.rank)

    @property
    def rankName(self):
        """Returns rank of card"""
        return Card.charToNameDict[self.rank]

    @property
    def suitName(self):
        """Returns suit of card"""
        return Card.charToNameDict[self.suit]

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

    def __str__(self):
        """Returns formatted representation of card"""
        return self.rankName + ' of ' + self.suitName

    def __repr__(self):
        """Returns canonical representation of card"""
        rank = str(self.rank)
        if self.isAce:
            rank = "'" + rank + "'"
        return "Card(%s, '%s')" % (rank, self.suit)

    def __eq__(self, other):
        """Returns True if self has equal rank and suit to that of other"""
        return self.rank == other.rank and self.suit == other.suit

    def __ne__(self, other):
        """Returns True iff self is not equal to other"""
        return not self == other

class Shoe:
    """Represents a shoe of decks for dealing purposes"""

    def __init__(self, n, algorithm, cutIndex=None):
        """Initializes shoe to have n decks,
               algorithm function for shuffling, and cutIndex"""
        self.cards = []
        self.numDecks = n
        self.algorithm = algorithm
        self.index = 0
        self.observers = []
        num_cards = get('NUM_CARDS_PER_DECK')
        if not cutIndex:
            self.cutIndex = int((n - 1/2) * num_cards)
        elif isinstance(cutIndex, float):
            self.cutIndex = int(floor(n * num_cards * cutIndex))
        elif cutIndex < 0:
            self.cutIndex = n * num_cards + cutIndex
        else:
            self.cutIndex = cutIndex
        for _ in range(n):
            self.cards.extend(Card.makeDeck())

    @property
    def numCardsRemainingToBeDealt(self):
        """Returns number of cards remaining to be dealt from shoe"""
        return self.cutIndex - self.index

    @property
    def numCardsRemainingInShoe(self):
        """Returns number of cards remaining in shoe"""
        return self.numDecks * get('NUM_CARDS_PER_DECK') - self.index

    @property
    def isExhausted(self):
        """Returns True iff all cards that will be dealt have been dealt"""
        return self.index >= self.cutIndex

    @property
    def isEmpty(self):
        """Returns True iff all cards in shoe have been dealt"""
        """This is only possible if cut index == len(self.cards)"""
        return self.index >= self.numDecks * get('NUM_CARDS_PER_DECK')

    def deal(self,n=1,visible=True):
        """Remove and return n cards from beginning of shoe"""
        c = []
        for _ in range(n):
            c.append(self.dealOneCard(visible))
        return c

    def burn(self,n=1):
        """Remove, without showing, n cards from beginning of shoe"""
        self.deal(n, False)

    def dealOneCard(self, visible=True):
        """Remove and return one card from beginning of shoe"""
        if self.isExhausted:
            self.shuffle()
        c = self.cards[self.index]
        if visible:
            self.notifyObservers(c)
        self.index += 1
        return c

    def shuffle(self):
        """Shuffles the deck using specified algorithm"""
        self.cards = self.algorithm(self.cards)
        self.index = 0
        self.notifyObservers(None)
        self.burn(get('NUM_CARDS_BURN_ON_SHUFFLE'))

    def registerObserver(self, observer):
        self.observers.append(observer)

    def unregisterObserver(self, observer):
        self.observers.remove(observer)

    def notifyObservers(self, card):
        for o in self.observers:
            o.update(card)

def faro_shuffle(deck):
    N = len(deck)//2
    ret = []
    for (a,b) in zip(deck[:N], deck[N:]):
        ret.append(a)
        ret.append(b)
    return ret

def fisher_yates_shuffle(deck):
    rand = Random()
    for i in range(len(deck) - 1, 1, -1):
        j = rand.randint(0, i)
        temp = deck[i]
        deck[i] = deck[j]
        deck[j] = temp
    return deck

class Hand(metaclass=ABCMeta):
    """Abstract base class for card hands"""

    @abstractmethod
    def value(self):
        """Returns largest value of hand"""
        raise NotImplementedError(
            'Hand implementations must implement the value method')

    @abstractmethod
    def numCards(self):
        """Returns number of cards in hand"""
        raise NotImplementedError(
            'Hand implementations must implement the numCards method')

    @abstractmethod
    def addCards(self, cards):
        """Adds list of cards to hand"""
        raise NotImplementedError(
            'Hand implementations must implement the addCards method')

    @abstractmethod
    def reset(self):
        """Resets hand to have no cards"""
        raise NotImplementedError(
            'Hand implementations must implement the reset method')

    @abstractmethod
    def __str__(self):
        """Returns canonical representation of hand"""
        raise NotImplementedError(
            'Hand implementations must implement the __str__ method')

class BlackjackHand(Hand):
    """Represents Blackjack hand"""

    HARD_ACE_VALUE = 11
    SOFT_ACE_VALUE = 1
    VALUES = [2,3,4,5,6,7,8,9,10,'A']

    def __init__(self):
        """Initializes hand to have no cards"""
        self.reset()

    @staticmethod
    def card_value(card):
        """Returns integer value of card"""
        if card.isAce:
            return BlackjackHand.HARD_ACE_VALUE
        elif card.isFaceCard:
            return 10
        return card.rank

    @property
    def value(self):
        """Returns largest non-bust value if possible, else largest value"""
        val = sum(BlackjackHand.card_value(c) for c in self.cards if not c.isAce)
        nAces = self.numAces
        if nAces > 0:
            val += (nAces - 1) * BlackjackHand.SOFT_ACE_VALUE
            if val + BlackjackHand.HARD_ACE_VALUE <= get('BLACKJACK_VALUE'):
                val += BlackjackHand.HARD_ACE_VALUE
            else:
                val += BlackjackHand.SOFT_ACE_VALUE
        return val

    @property
    def ranks(self):
        """Returns list of ranks in hand"""
        return [c.rank for c in self.cards]

    @property
    def isAcePair(self):
        """Return True iff hand is pair of Aces"""
        return self.numCards == 2 and self.numAces == 2

    @property
    def isSoft17(self):
        """Return True iff hand is soft 17"""
        return self.value == 17 and self.isSoft

    @property
    def isSoft(self):
        """Return True iff hand is soft (i.e. contains hard-valued ace)"""
        val = sum(BlackjackHand.card_value(c) for c in self.cards if not c.isAce)
        numAces = self.numAces
        if numAces > 0:
            val += (numAces - 1) * BlackjackHand.SOFT_ACE_VALUE
            if val + BlackjackHand.HARD_ACE_VALUE <= get('BLACKJACK_VALUE'):
                return True
        return False

    @property
    def numCards(self):
        """Returns number of cards in hand"""
        return len(self.cards)

    @property
    def numAces(self):
        """Returns number of ace cards in hand"""
        return sum(1 for c in self.cards if c.isAce)

    @property
    def isBlackjackValued(self):
        """Returns True iff hand has value equal to Blackjack value"""
        return self.value == get('BLACKJACK_VALUE')

    @property
    def isNaturalBlackjack(self):
        """Returns True iff hand is natural blackjack
        Note a blackjack after split is NOT considered natural"""
        return (self.numCards == 2 and
                self.value == get('BLACKJACK_VALUE') and
                not self.wasSplit)

    @property
    def isPairByRank(self):
        """Returns True iff initial two cards are equal in rank"""
        return (self.numCards == 2 and
                self.cards[0].rankEquivalent(self.cards[1]))

    @property
    def isPairByValue(self):
        """Returns True iff initial two cards are equal in rank"""
        v1 = BlackjackHand.card_value(self.cards[0])
        v2 = BlackjackHand.card_value(self.cards[1])
        return self.numCards == 2 and v1 == v2

    @property
    def isPair(self):
        """Returns True iff this hand is a pair"""
        if get('SPLIT_BY_VALUE'):
            return self.isPairByValue
        return self.isPairByRank

    @property
    def isBust(self):
        """Returns True iff hand value is greater than blackjack value"""
        return self.value > get('BLACKJACK_VALUE')

    @property
    def hasAce(self):
        """Returns True iff hand has at least one ace"""
        return self.numAces >= 1

    @property
    def splitCards(self):
        """Returns cards as tuple"""
        if self.numCards > 2:
            raise Exception('Cannot split hand of more than 2 cards')
        return tuple(self.cards)

    @property
    def description(self):
        """Returns description of hand"""
        if self.isPair:
            return 'pair of %ss' % self.cards[0].rank
        value = str(self.value)
        if self.isSoft:
            return 'soft ' + value
        return value

    def addCards(self, *cards):
        """Adds args to hand"""
        self.cards.extend(cards)

    def reset(self):
        """Removes all cards from hand"""
        self.cards = []
        self.wasSplit = False

    def __eq__(self, other):
        """Returns True iff cards in self are same as in other"""
        if self.numCards != other.numCards:
            return False
        for c1 in self.cards:
            if not c1 in other.cards:
                return False
        return True

    def __str__(self):
        """Returns comma delimited list of cards' representations"""
        return '[' + ', '.join(str(c) for c in self.cards) +']'

    def __repr__(self):
        """Returns comma delimited list of cards' representations"""
        return '[' + ', '.join(repr(c) for c in self.cards) +']'

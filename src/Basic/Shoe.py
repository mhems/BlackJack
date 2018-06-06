from math import floor
from random import Random

from src.Basic.Card import Card
from src.Utilities.config import get

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
        if not cutIndex:
            self.cutIndex = int((n - 1/2) * Card.NUM_CARDS_PER_DECK)
        elif isinstance(cutIndex, float):
            self.cutIndex = int(floor(n * Card.NUM_CARDS_PER_DECK * cutIndex))
        elif cutIndex < 0:
            self.cutIndex = n * Card.NUM_CARDS_PER_DECK + cutIndex
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
        return self.numDecks * Card.NUM_CARDS_PER_DECK - self.index

    @property
    def isExhausted(self):
        """Returns True iff all cards that will be dealt have been dealt"""
        return self.index >= self.cutIndex

    @property
    def isEmpty(self):
        """Returns True iff all cards in shoe have been dealt"""
        """This is only possible if cut index == len(self.cards)"""
        return self.index >= self.numDecks * Card.NUM_CARDS_PER_DECK

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

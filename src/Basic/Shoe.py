####################
#
# Shoe.py
#
####################

from math   import floor
from random import Random

from src.Basic.Card import Card
from src.Utilities.Configuration import Configuration

class Shoe:
    """Represents a shoe of decks for dealing purposes"""

    def __init__(self,n,algorithm,cutIndex=None):
        """Initializes shoe to have n decks,
               algorithm function for shuffling, and cutIndex"""
        self.__cards = []
        self.numDecks = n
        self.__algorithm = algorithm
        self.__index = 0
        self.__observers = []
        if not cutIndex:
            self.cutIndex = int((n - 1/2) * Card.NUM_CARDS_PER_DECK)
        elif isinstance(cutIndex,float):
            self.cutIndex = int(floor(n * Card.NUM_CARDS_PER_DECK * cutIndex))
        elif cutIndex < 0:
            self.cutIndex = n * Card.NUM_CARDS_PER_DECK + cutIndex
        else:
            self.cutIndex = cutIndex
        for _ in range(n):
            self.__cards.extend(Card.makeDeck())

    @property
    def numCardsRemainingToBeDealt(self):
        """Returns number of cards remaining to be dealt from shoe"""
        return self.cutIndex - self.__index

    @property
    def numCardsRemainingInShoe(self):
        """Returns number of cards remaining in shoe"""
        return self.numDecks * Card.NUM_CARDS_PER_DECK - self.__index
    
    @property
    def isExhausted(self):
        """Returns True iff all cards that will be dealt have been dealt"""
        return self.__index >= self.cutIndex

    @property
    def isEmpty(self):
        """Returns True iff all cards in shoe have been dealt"""
        """This is only possible if cut index == len(self.__cards)"""
        return self.__index >= self.numDecks * Card.NUM_CARDS_PER_DECK

    def deal(self,n=1):
        """Remove and return n cards from beginning of shoe"""
        c = []
        for _ in range(n):
            c.append(self.dealOneCard())
        return c
    
    def dealOneCard(self):
        """Convenience method to deal one card"""
        if self.isExhausted:
            self.shuffle()
            self.notifyObservers(None)
        c = self.__cards[self.__index]
        self.notifyObservers(c)
        self.__index += 1
        return c

    def shuffle(self):
        """Shuffles the deck using specified algorithm"""
        self.__cards = self.__algorithm(self.__cards)
        self.__index = 0
        self.deal(Configuration.get('NUM_CARDS_BURN_ON_SHUFFLE'))        

    def registerObserver(self, observer):
        self.__observers.append(observer)

    def unregisterObserver(self, observer):
        self.__observers.remove(observer)
        
    def notifyObservers(self, card):
        for o in self.__observers:
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
        temp    = deck[i]
        deck[i] = deck[j]
        deck[j] = temp
    return deck

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
        self.rank = rank
        self.suit = suit
        if self.rank not in Card.ranks:
            raise TypeError("Rank must be a number 2-10 or J, Q, K, A (Jack, Queen, King, or Ace)")
        if self.suit not in Card.suits:
            raise TypeError("Suit must be one of S, H, D, C (Spades, Hearts, Diamonds, Clubs)")
        
    def __str__(self):
        return str(Card.__charToNameDict[self.rank]) + ' of ' + Card.__charToNameDict[self.suit]

    def __repr__(self):
        return self.rank + ' of ' + self.suit

if __name__ == '__main__':
    c = Card(4,'D')
    print(c)
    #d = Card(4,'E')

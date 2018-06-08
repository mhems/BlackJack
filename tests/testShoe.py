import unittest

from cards import (Card, Shoe)

def alg(cards):
    cards.reverse()
    return cards

class testShoe(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInit(self):
        s = Shoe(1,alg)
        self.assertEqual(s.numDecks,1,'testShoe:testInit:Number of decks not initialized properly')
        self.assertEqual(s.cutIndex,26,'testShoe:testInit:Cut index not default initialized')
        s = Shoe(2,alg)
        self.assertEqual(s.cutIndex,78,'testShoe:testInit:Cut index not default initialized')
        s = Shoe(4,alg,200)
        self.assertEqual(s.numDecks,4,'testShoe:testInit:Number of decks not initialized properly')
        self.assertEqual(s.cutIndex,200,'testShoe:testInit:Cut index not initialized properly')
        s = Shoe(6,alg,0.75)
        self.assertEqual(s.cutIndex,234,'testShoe:testInit:Cut index not calculated properly')

    def testDeal(self):
        s = Shoe(2,alg)
        c = s.deal()
        self.assertTrue(isinstance(c,list),'testShoe:testDeal:Deal should return list of card')
        self.assertTrue(isinstance(c[0],Card),'testShoe:testDeal:List should be comprised of cards')
        c = s.deal(4)
        self.assertEqual(len(c),4,'testShoe:testDeal:Deal should return list of 4 cards')
        c = s.deal(2*52-5-26)
        c = s.deal()[0]
        self.assertEqual(c,Card('A','D'),'testShoe:testDeal:Deal at end of shoe should prompt shuffle')

    def testDealOneCard(self):
        s = Shoe(3,alg,150)
        for i in range(150):
            c = s.dealOneCard()
            self.assertTrue(isinstance(c,Card),'testShoe:testDealOneCard:Deal one card should return one card')
        c = s.dealOneCard()
        self.assertEqual(c,Card('A','D'),'testShoe:testDealOneCard:Deal should prompt shuffle')
        c = s.dealOneCard()
        self.assertEqual(c,Card('A','H'),'testShoe:testDealOneCard:Deal should deal in order after shuffle')

    def testNumCardsRemainingToBeDealt(self):
        s = Shoe(3,alg)
        self.assertEqual(s.numCardsRemainingToBeDealt,3*52-26,'testShoe:testNumCardsRemainingToBeDealt:Undealt deck should have all cards remaining to be dealt')
        for _ in range(6):
            s.dealOneCard()
        self.assertEqual(s.numCardsRemainingToBeDealt,3*52-26-6,'testShoe:testNumCardsRemainingToBeDealt:Partially dealt deck should have most cards remaining to be dealt')
        for _ in range(3*52-26-6):
            s.dealOneCard()
        self.assertEqual(s.numCardsRemainingToBeDealt,0,'testShoe:testNumCardsRemainingToBeDealt:Fully dealt deck should have no cards remaining to be dealt')
        s.dealOneCard()
        self.assertEqual(s.numCardsRemainingToBeDealt,3*52-26-2,'testShoe:testNumCardsRemainingToBeDealt:Newly shuffled deck should have all but one card remaining to be dealt')

    def testNumCardsRemainingInShoe(self):
        s = Shoe(3,alg)
        self.assertEqual(s.numCardsRemainingInShoe,3*52,'testShoe:testNumCardsRemainingInShoe:Undealt deck should have all cards remaining in shoe')
        for _ in range(6):
            s.dealOneCard()
        self.assertEqual(s.numCardsRemainingInShoe,3*52-6,'testShoe:testNumCardsRemainingInShoe:Partially dealt deck should have most cards plus cut cards remaining in shoe')
        for _ in range(3*52-26-6):
            s.dealOneCard()
        self.assertEqual(s.numCardsRemainingInShoe,26,'testShoe:testNumCardsRemainingInShoe:Fully dealt deck should have only cut cards left in shoe')
        s.dealOneCard()
        self.assertEqual(s.numCardsRemainingInShoe,3*52-2,'testShoe:testNumCardsRemainingInShoe:Newly shuffled deck should have all but one card remaining in shoe')

    def testIsExhausted(self):
        s = Shoe(3,alg)
        self.assertFalse(s.isExhausted,'testShoe:testIsExhausted:Fresh deck should not be exhausted')
        for _ in range(6):
            s.dealOneCard()
        self.assertFalse(s.isExhausted,'testShoe:testIsExhausted:Partially dealt deck should not be exhausted')
        for _ in range(3*52-26-6):
            s.dealOneCard()
        self.assertTrue(s.isExhausted,'testShoe:testIsExhausted:Dealt deck should be exhausted')
        s.dealOneCard()
        self.assertFalse(s.isExhausted,'testShoe:testIsExhausted:New deck should not be exhausted')

    def testIsEmpty(self):
        s = Shoe(3,alg,3*52)
        self.assertFalse(s.isEmpty,'testShoe:testIsEmpty:Fresh deck should not be empty')
        for _ in range(6):
            s.dealOneCard()
        self.assertFalse(s.isEmpty,'testShoe:testIsEmpty:Partially dealt deck should not be empty')
        for _ in range(3*52-6):
            s.dealOneCard()
        self.assertTrue(s.isEmpty,'testShoe:testIsEmpty:Dealt deck should be empty')
        s.dealOneCard()
        self.assertFalse(s.isEmpty,'testShoe:testIsEmpty:New deck should not be empty')

if __name__ == '__main__':
    unittest.main()

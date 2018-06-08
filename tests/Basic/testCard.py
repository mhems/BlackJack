import unittest

from src.Basic.cards import Card
# from itertools import *

class testCard(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInit(self):
        c = Card(4,'H')
        self.assertEqual(c.rank,4,"testCard:testInit:Card rank not initialized properly")
        self.assertEqual(c.suit,'H',"testCard:testInit:Card suit not initialized properly")
        self.assertRaises(TypeError,Card.__init__,'B','D')
        self.assertRaises(TypeError,Card.__init__,'K','B')
        c1 = Card(4,'hearts')
        c2 = Card(4,'h')
        c3 = Card(4,'Hearts')

    def testRank(self):
        c = Card('J','H')
        self.assertEqual(c.rank,'J','testCard:testRank:Card rank doesn\'t evaluate properly')

    def testSuit(self):
        c = Card(10,'H')
        self.assertEqual(c.suit,'H','testCard:testRank:Card suit doesn\'t evaluate properly')

    def testStr(self):
        c = Card('A','S')
        self.assertEqual(str(c),'Ace of Spades','testCard:testStr: str not working')

    def testRepr(self):
        c = Card('A','S')
        self.assertEqual(repr(c),'Ace of Spades','testCard:testStr: repr not working')

    def testEQ(self):
        c = Card(4,'H')
        c1 = Card(4,'hearts')
        c2 = Card(4,'h')
        c3 = Card(4,'Hearts')
        self.assertTrue(c  == c1,'testCard:testEq:Cards should be equal')
        self.assertTrue(c1 == c2,'testCard:testEq:Cards should be equal')
        self.assertTrue(c2 == c3,'testCard:testEq:Cards should be equal')
        a = Card('A','S')
        self.assertFalse(c == a,'testCard:testEq:Cards should not be equal')

    def testNE(self):
        c  = Card(4, 'H')
        c1 = Card(4, 'C')
        self.assertTrue(c != c1,'testCard:testNe:Cards should not be equal')
        c3 = Card(5, 'H')
        self.assertTrue(c != c3,'testCard:testNe:Cards should not be equal')
        c4 = Card(4, 'h')
        self.assertFalse(c != c4,'testCard:testNe:Cards should be equal')

    def testRankEquivalent(self):
        c = Card(4,'H')
        c1 = Card(4, 'D')
        self.assertTrue(c.rankEquivalent(c1),'testCard:testRankEq:Cards should have same rank')
        c = Card('J','H')
        c1 = Card('K','D')
        self.assertFalse(c.rankEquivalent(c1),'testCard:testRankEq:Cards should not have same rank')

    def testIsAce(self):
        c = Card('A','H')
        self.assertTrue(c.isAce,'testCard:testIsAce:Ace should return True')
        n = Card(9,'H')
        self.assertFalse(n.isAce,'testCard:testIsAce:Non-ace should return False')

    def testIsFaceCard(self):
        k = Card('K','C')
        self.assertTrue(k.isFaceCard,'testCard:testFaceCard:King should return True')
        a = Card('A','C')
        self.assertTrue(a.isFaceCard,'testCard:testFaceCard:Ace should return True')
        t = Card(10,'C')
        self.assertFalse(t.isFaceCard,'testCard:testFaceCard:Non-face card should return False')

    def testMakeDeck(self):
        d = Card.makeDeck()
        self.assertEqual(len(d),52,'testCard:testMakeDeck:Deck should have 52 cards')
        self.assertEqual(len(list(filter(lambda c:c.suit=='H',d))),13,'testCard:testMakeDeck:Deck should have 13 cards of hearts suit')
        self.assertEqual(len(list(filter(lambda c:c.rank=='A',d))),4,'testCard:testMakeDeck:Deck should have 4 aces')

if __name__ == '__main__':
    unittest.main()

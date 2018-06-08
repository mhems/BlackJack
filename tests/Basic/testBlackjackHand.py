import unittest

from src.Basic.cards import (Card, BlackjackHand)

class testBlackjackHand(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInit(self):
        h = BlackjackHand()
        self.assertEqual(h.numCards,0,'testBlackjackHand:testInit:New Hand should be empty')

    def testValue(self):
        h = BlackjackHand()
        self.assertEqual(h.value,0,'testBlackjackHand:testValue:New hand should have value 0')
        h.addCards(Card('A','D'), Card(4,'D'))
        self.assertEqual(h.value,15,'testBlackjackHand:testValue:Soft 15 should have value 15')
        h.addCards(Card('J','D'))
        self.assertEqual(h.value,15,'testBlackjackHand:testValue:Hard 15 should have value 15')
        h.addCards(Card(6,'D'))
        self.assertEqual(h.value,21,'testBlackjackHand:testValue:21 should have value 21')
        h = BlackjackHand()
        h.addCards(Card('A','D'), Card('A','H'))
        self.assertEqual(h.value,12,'testBlackjackHand:testValue:Soft 12 should have value 12')
        h.addCards(Card('Q','H'))
        self.assertEqual(h.value,12,'testBlackjackHand:testValue:Hard 12 should have value 12')
        h.addCards(Card(9,'D'))
        self.assertEqual(h.value,21,'testBlackjackHand:testValue:21 should have value 21')

    def testRanks(self):
        h = BlackjackHand()
        h.addCards(Card(9,'D'), Card(10,'H'))
        self.assertEqual(h.ranks,[9,10],'testBlackjackHand:testRanks:Hand with 9 and 10 should have ranks 9 and 10')
        h = BlackjackHand()
        h.addCards(Card('K','H'), Card('A','C'))
        self.assertEqual(h.ranks,['K','A'],'testBlackjackHand:testRanks:Hand with King and Ace should have ranks King and Ace')
        self.assertNotEqual(h.ranks,[10,'A'],'testBlackjackHand:testRanks:Ranks should not return values')

    def testSoft(self):
        h = BlackjackHand()
        h.addCards(Card('A','D'), Card(10,'D'))
        self.assertTrue(h.isSoft,'testBlackjackHand:testSoft:A,10 should be soft')
        h.addCards(Card(10,'H'))
        self.assertFalse(h.isSoft,'testBlackjackHand:testSoft:A,10,10 should not be soft')
        h = BlackjackHand()
        h.addCards(Card('A','D'), Card(3,'C'), Card(5,'H'))
        self.assertTrue(h.isSoft,'testBlackjackHand:testSoft:A,3,5 should be soft')
        h = BlackjackHand()
        h.addCards(Card('A','D'), Card('A','D'))
        self.assertTrue(h.isSoft,'testBlackjackHand:testSoft:A,A should be soft')
        h.addCards(Card(10,'D'))
        self.assertFalse(h.isSoft,'testBlackjackHand:testSoft:A,A,10 should not be soft')
        h = BlackjackHand()
        h.addCards(Card(10,'D'), Card(6,'H'))
        self.assertFalse(h.isSoft,'testBlackjackHand:testSoft:10,5 should not be soft')

    def testIsAcePair(self):
        h = BlackjackHand()
        h.addCards(Card('A','D'), Card('A','H'))
        self.assertTrue(h.isAcePair,'testBlackjackHand:testIsAcePair:A,A should be ace pair')
        h.addCards(Card(4,'D'))
        self.assertFalse(h.isAcePair,'testBlackjackHand:testIsAcePair:A,A,4 should not be ace pair')
        h = BlackjackHand()
        h.addCards(Card('A','C'), Card('J', 'D'))
        self.assertFalse(h.isAcePair,'testBlackjackHand:testIsAcePair:A,J should not be ace pair')
        h = BlackjackHand()
        h.addCards(Card('J','C'), Card(10, 'H'))
        self.assertFalse(h.isAcePair,'testBlackjackHand:testIsAcePair:J,10 should not be ace pair')

    def testIsSoft17(self):
        h = BlackjackHand()
        h.addCards(Card('A','D'), Card(6,'D'))
        self.assertTrue(h.isSoft17,'testBlackjackHand:testSoft17:A,6 should be soft 17')
        h = BlackjackHand()
        h.addCards(Card('A','D'), Card(3,'C'), Card(3,'H'))
        self.assertTrue(h.isSoft17,'testBlackjackHand:testSoft17:A,3,3 should be soft 17')
        h = BlackjackHand()
        h.addCards(Card(10,'D'), Card(7,'C'))
        self.assertFalse(h.isSoft17,'testBlackjackHand:testSoft17:10,7 should not be soft 17')

    def testNumCards(self):
        # Also tests addCards
        h = BlackjackHand()
        self.assertEqual(h.numCards,0,'testBlackjackHand:testNumCards:New hand should have no cards')
        h.addCards(Card(4,'C'))
        self.assertEqual(h.numCards,1,'testBlackjackHand:testNumCards:Hand should have one card')
        h.addCards(Card(5,'D'))
        self.assertEqual(h.numCards,2,'testBlackjackHand:testNumCards:Hand should have two cards')
        h.addCards(Card(4,'D'), Card(6,'H'))
        self.assertEqual(h.numCards,4,'testBlackjackHand:testNumCards:Hand should have four cards')

    def testNumAces(self):
        h = BlackjackHand()
        self.assertEqual(h.numAces,0,'testBlackjackHand:testNumAces:New hand should have no aces')
        h.addCards(Card(5,'H'), Card(10,'D'))
        self.assertEqual(h.numAces,0,'testBlackjackHand:testNumAces:Hand without aces should have no aces')
        h.addCards(Card('A','S'))
        self.assertEqual(h.numAces,1,'testBlackjackHand:testNumAces:Hand with an ace should have one ace')

        h.addCards(Card('A','H'))
        self.assertEqual(h.numAces,2,'testBlackjackHand:testNumAces:Hand with two aces should have two aces')

    def testIsNaturalBlackjack(self):
        h = BlackjackHand()
        self.assertFalse(h.isNaturalBlackjack,'testBlackjackHandValued:testIsNaturalBlackjack:New hand is not a natural blackjack')
        h.addCards(Card('A','S'), Card(10,'H'))
        self.assertTrue(h.isNaturalBlackjack,'testBlackjackHand:testIsNaturalBlackJack:Blackjack should be a natural blackjack')
        h.addCards(Card('J','S'))
        self.assertFalse(h.isNaturalBlackjack,'testBlackjackHand:testIsNaturalBlackjack:Non-initial blackjack should not be natural blackjack')
        h = BlackjackHand()
        h.addCards(Card('J','S'), Card(4,'D'))
        self.assertFalse(h.isNaturalBlackjack,'testBlackjackHand:testIsNaturalBlackjack:Non-21 hand should not be natural blackjack')

    def testIsPairByRank(self):
        h = BlackjackHand()
        h.addCards(Card(4,'D'), Card(4,'H'))
        self.assertTrue(h.isPairByRank,'testBlackjackHand:testIsPairByRank:Pair of 4s should be a pair by rank')
        h = BlackjackHand()
        h.addCards(Card(10,'D'), Card('J','D'))
        self.assertFalse(h.isPairByRank,'testBlackjackHand:testIsPairByRank:Ten and Jack should not be pair by rank')

    def testIsPairByValue(self):
        h = BlackjackHand()
        h.addCards(Card(4,'D'), Card(4,'H'))
        self.assertTrue(h.isPairByValue,'testBlackjackHand:testIsPairByValue:Pair of 4s should be a pair by value')
        h = BlackjackHand()
        h.addCards(Card(10,'D'), Card('J','D'))
        self.assertTrue(h.isPairByValue,'testBlackjackHand:testIsPairByValue:Ten and Jack should be pair by value')
        h = BlackjackHand()
        h.addCards(Card('A','D'), Card('J','D'))
        self.assertFalse(h.isPairByValue,'testBlackjackHand:testIsPairByValue:Ace and Jack should not be pair by value')

    def testIsBust(self):
        h = BlackjackHand()
        self.assertFalse(h.isBust,'testBlackjackHand:testIsBust:New hand should not be bust')
        h.addCards(Card('J','D'), Card('K','D'))
        self.assertFalse(h.isBust,'testBlackjackHand:testIsBust:Hand with value 20 should not be bust')
        h.addCards(Card(2,'D'))
        self.assertTrue(h.isBust,'testBlackjackHand:testIsBust:Bust hand should be bust')
        h = BlackjackHand()
        h.addCards(Card('A','D'), Card(7,'D'))
        self.assertFalse(h.isBust,'testBlackjackHand:testIsBust:Soft 18 should not be bust')
        h.addCards(Card(10,'D'))
        self.assertFalse(h.isBust,'testBlackjackHand:testIsBust:Hard 18 should not be bust')

    def testHasAce(self):
        h = BlackjackHand()
        self.assertFalse(h.hasAce,'testBlackjackHand:testHasAce:New hand should have no ace')
        h.addCards(Card('A','S'), Card(4,'D'))
        self.assertTrue(h.hasAce,'testBlackjackHand:testHasAce:Hand with ace should have an ace')
        h.addCards(Card('A','D'))
        self.assertTrue(h.hasAce,'testBlackjackHand:testHasAce:Hand with multiple aces should have an ace')

    def testReset(self):
        h = BlackjackHand()
        h.addCards(Card('A','S'), Card(4,'D'))
        h.reset()
        self.assertEqual(h.numCards,0,'testBlackjackHand:testReset:Reset hand should have no cards')

    def testStr(self):
        h = BlackjackHand()
        self.assertEqual(str(h),'[]','testBlackjackHand:testStr:New hand should have empty string')
        h.addCards(Card('A','S'), Card(4,'D'))
        self.assertEqual(str(h),'[Ace of Spades, 4 of Diamonds]', 'testBlackjackHand:testStr:Hand\'s string should list cards in hand')

if __name__ == '__main__':
    unittest.main()

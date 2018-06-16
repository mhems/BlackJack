import unittest

from config import (Config, SemanticConfigError)

class testConfiguration(unittest.TestCase):

    def setUp(self):
        self.cfg = Config.load()

    def testNegPosInt(self):
        with self.assertRaises(SemanticConfigError):
            self.cfg['BLACKJACK_VALUE'] = -2

    def testZeroPos(self):
        with self.assertRaises(SemanticConfigError):
            self.cfg['BLACKJACK_VALUE'] = 0

    def testBadBool(self):
        with self.assertRaises(SemanticConfigError):
            self.cfg['PUSH_ON_BLACKJACK'] = 5

    def testOverBurn(self):
        with self.assertRaises(SemanticConfigError):
            self.cfg['NUM_DECKS'] = 1
            self.cfg['NUM_CARDS_BURN_ON_SHUFFLE'] = -54

    def testOverCut(self):
        with self.assertRaises(SemanticConfigError):
            self.cfg['NUM_DECKS'] = 1
            self.cfg['CUT_INDEX'] = -54

    def testBadRatio(self):
        with self.assertRaises(SemanticConfigError):
            self.cfg['PAYOUT_RATIO'] = '1/2/3'

    def testNegRatio(self):
        with self.assertRaises(SemanticConfigError):
            self.cfg['PAYOUT_RATIO'] = -1

    def testBadRange(self):
        with self.assertRaises(SemanticConfigError):
            self.cfg['TOTALS_ALLOWED_FOR_DOUBLE'] = ['A', 10]

    def testBadMaxBet(self):
        with self.assertRaises(SemanticConfigError):
            self.cfg['MINIMUM_BET'] = 5
            self.cfg['MAXIMUM_BET'] = 4

if __name__ == '__main__':
    unittest.main()

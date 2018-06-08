import unittest

from config import get
from policies import MinBettingStrategy

class testMinBettingStrategy(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testBet(self):
        strat = MinBettingStrategy()
        self.assertEqual(strat.bet(), get('MINIMUM_BET'), 'testMinBettingStrategy:testBet:Bet should always be minimum')

if __name__ == '__main__':
    unittest.main()

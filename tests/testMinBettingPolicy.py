import unittest

from config import get
from policies import MinBettingPolicy

class testMinBettingPolicy(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testBet(self):
        strat = MinBettingPolicy()
        self.assertEqual(strat.bet(), get('MINIMUM_BET'), 'testMinBettingPolicy:testBet:Bet should always be minimum')

if __name__ == '__main__':
    unittest.main()

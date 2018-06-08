import unittest

from src.policies import MinBettingStrategy
from src.config import get

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

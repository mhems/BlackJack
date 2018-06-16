import unittest

from config import Config
from policies import MinBettingPolicy

class testMinBettingPolicy(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testBet(self):
        cfg = Config.load()
        strat = MinBettingPolicy()
        self.assertEqual(strat.bet(), cfg['MINIMUM_BET'], 'testMinBettingPolicy:testBet:Bet should always be minimum')

if __name__ == '__main__':
    unittest.main()

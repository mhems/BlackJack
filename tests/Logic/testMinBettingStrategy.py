import unittest

from src.Logic.policies import MinBettingStrategy
import src.Utilities.Configuration as config

class testMinBettingStrategy(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testBet(self):
        strat = MinBettingStrategy()
        self.assertEqual(strat.bet(), config.get('MINIMUM_BET'), 'testMinBettingStrategy:testBet:Bet should always be minimum')

if __name__ == '__main__':
    unittest.main()

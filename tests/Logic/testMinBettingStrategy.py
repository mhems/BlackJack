####################
#
# testMinBettingStrategy.py
#
####################

import unittest

from src.Logic.MinBettingStrategy import MinBettingStrategy
from src.Utilities.Configuration  import Configuration

class testMinBettingStrategy(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testBet(self):
        strat = MinBettingStrategy()
        self.assertEqual(strat.bet(), Configuration.get('MINIMUM_BET'), 'testMinBettingStrategy:testBet:Bet should always be minimum')

if __name__ == '__main__':
    unittest.main()

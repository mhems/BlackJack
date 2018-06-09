import unittest

from cards import (Card, BlackjackHand)
from commands import Command
from config import (get, loadConfiguration)
from policies import DealerPolicy

class testDealerPolicy(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDecide(self):
        cmds = [Command.HIT, Command.STAND]
        policy = DealerPolicy()
        hand = BlackjackHand()
        # 4 through 12
        for i in range(2, 11):
            hand.addCards(Card(2,'H'), Card(i,'H'))
            self.assertEqual(policy.decide(hand, None, cmds), Command.HIT, 'testDealerPolicy:testDecide:Dealer should hit on 16 and less')
            hand.reset()
        # 13 through 16
        for i in range(3, 7):
            hand.addCards(Card(10,'H'), Card(i,'H'))
            self.assertEqual(policy.decide(hand, None, cmds), Command.HIT, 'testDealerPolicy:testDecide:Dealer should hit on 16 and less')
            hand.reset()
        # 17 through 20
        for i in range(7, 11):
            hand.addCards(Card(10,'H'), Card(i,'H'))
            self.assertEqual(policy.decide(hand, None, cmds), Command.STAND, 'testDealerPolicy:testDecide:Dealer should stand on hard 17 through 20')
            hand.reset()
        # soft 17
        hand.addCards(Card('A', 'H'), Card(6, 'H'))
        self.assertEqual(policy.decide(hand, None, cmds), Command.HIT, 'testDealerPolicy:testDecide:Dealer should hit on soft 17 if configured to do so')
        loadConfiguration('cfg/S17_false.ini')
        self.assertEqual(policy.decide(hand, None, cmds), Command.STAND, 'testDealerPolicy:testDecide:Dealer should stand on soft 17 if configured to do so')

if __name__ == '__main__':
    unittest.main()

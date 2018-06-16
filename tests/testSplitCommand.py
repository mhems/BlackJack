import unittest

from cards import (Card,
                       BlackjackHand,
                       Shoe)
from commands import (HitCommand,
                      StandCommand,
                      DoubleCommand,
                      SplitCommand)
from config import cfg
from game import Player
from policies import MinBettingPolicy
from table import TableSlot

class testSplitCommand(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPerform(self):
        slot = TableSlot()
        player = Player("Test", None, None, MinBettingPolicy())
        slot.seatPlayer(player)
        shoe = Shoe(1,lambda x:x)
        hitCmd = HitCommand(shoe)
        standCmd = StandCommand()
        splitCmd = SplitCommand(hitCmd, standCmd)
        player.receive_payment(cfg['MINIMUM_BET'] *
                               (1 + cfg['SPLIT_RATIO']))
        slot.addCards(Card(5,'C'), Card(5,'H'))
        slot.promptBet()
        rc = splitCmd.perform(slot)
        self.assertFalse(rc, 'testSplitCommand:testPerform:Split should not end hand')
        self.assertEqual(player.stack.amount, 0, 'testSplitCommand:testPerform:Split should deduct appropriate amount from player')
        hands = slot.hands
        self.assertEqual(len(hands), 2, 'testSplitCommand:testPerform:Split should split player\'s hand into two hands')
        self.assertTrue(hands[0].wasSplit, 'testSplitCommand:testPerform: Split hands should reflect split')
        self.assertTrue(hands[1].wasSplit, 'testSplitCommand:testPerform: Split hands should reflect split')
        expected = BlackjackHand()
        expected.addCards(Card(5,'C'), Card(2, 'S'))
        self.assertEqual(hands[0], expected, 'testSplitCommand:testPerform:Split hands should draw next card from shoe')
        expected.reset()
        expected.addCards(Card(5,'H'), Card(2, 'H'))
        self.assertEqual(hands[1], expected, 'testSplitCommand:testPerform:Split hands should draw next card from shoe')

    def testIsAvailable(self):
        slot = TableSlot()
        player = Player("Test", None, None, MinBettingPolicy())
        slot.seatPlayer(player)
        shoe = Shoe(1,lambda x:x)
        hitCmd = HitCommand(shoe)
        standCmd = StandCommand()
        splitCmd = SplitCommand(hitCmd, standCmd)
        player.receive_payment(cfg['MINIMUM_BET'])
        slot.addCards(Card(5,'C'), Card(6,'C'))
        slot.promptBet()
        self.assertFalse(splitCmd.isAvailable(slot), 'testSplitCommand:testIsAvailable:Split should not be available to insufficiently funded player')
        player.receive_payment(cfg['MINIMUM_BET'] *
                               (1 + cfg['SPLIT_RATIO']))
        slot.promptBet()
        self.assertFalse(splitCmd.isAvailable(slot), 'testSplitCommand:testIsAvailable:Split should not be avaible to non-pair hand')

        slot.clearHands()
        slot.addCards(Card(10,'C'), Card('K','C'))
        self.assertFalse(splitCmd.isAvailable(slot), 'testSplitCommand:testIsAvailable:Split should not be available to non rank-paired hand when split by value is disallowed')
        slot.clearHands()
        cfg.mergeFile('cfg/split_by_value.ini')
        slot.addCards(Card(10,'C'), Card('K','C'))
        self.assertTrue(splitCmd.isAvailable(slot), 'testSplitCommand:testIsAvailable:Split should be availabe to non rank-paired hand when split by value is allowed')

        hitCmd.perform(slot)
        player.receive_payment(cfg['MINIMUM_BET'])
        cfg.reset()
        self.assertFalse(splitCmd.isAvailable(slot), 'testSplitCommand:testIsAvailable:Split should not be availabe to hand beyond first action')
        cfg.mergeFile('cfg/resplit_upto.ini')
        slot.clearHands()
        slot.promptBet()
        slot.addCards(Card(5,'C'), Card(5,'C'))
        self.assertFalse(splitCmd.isAvailable(slot), 'testSplitCommand:testIsAvailable:Split should not be availabe if splitting is disallowed')

        player.receive_payment(3 * cfg['MINIMUM_BET'] * cfg['SPLIT_RATIO'])
        slot.clearHands()
        slot.promptBet()
        slot.addCards(Card('A','C'), Card('A','H'))
        splitCmd.perform(slot)
        slot.hands[0].cards = []
        slot.hands[0].addCards(Card('A', 'C'), Card('A', 'D'))
        cfg.reset()
        cfg.mergeFile('cfg/resplit_aces.ini')
        self.assertFalse(splitCmd.isAvailable(slot), 'testSplitCommand:testIsAvailable:Split should not be available if hand is aces from split and resplitting aces is disallowed')

        player.receive_payment(cfg['MINIMUM_BET'] *
                               (2 + cfg['SPLIT_RATIO']))
        cfg.reset()
        self.assertTrue(splitCmd.isAvailable(slot), 'testSplitCommand:testIsAvailable:Split should be available on split aces if resplit aces allowed')

if __name__ == '__main__':
    unittest.main()

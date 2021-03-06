import unittest

from cards import (Card, Shoe)
from commands import (DoubleCommand,
                      HitCommand,
                      StandCommand,
                      SplitCommand)
from config import cfg
from game import Player
from policies import MinBettingPolicy
from table import TableSlot

class testDoubleCommand(unittest.TestCase):
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
        doubleCmd = DoubleCommand(hitCmd, standCmd)
        player.receive_payment(cfg['MINIMUM_BET'] *
                               (1 + cfg['DOUBLE_RATIO']))
        slot.promptBet()
        rc = doubleCmd.perform(slot)
        self.assertEqual(player.stack.amount, 0, 'testDoubleCommand:testPerform:Double should remove amount in pot from player')
        self.assertTrue(rc, 'testDoubleCommand:testPerform:Double should always end hand')
        self.assertEqual(slot.hand.value, 2, 'testDoubleCommand:testPerform:Double should add next card in shoe to hand')

    def testIsAvailable(self):
        slot = TableSlot()
        player = Player("Test", None, None, MinBettingPolicy())
        shoe = Shoe(1,lambda x:x)
        hitCmd = HitCommand(shoe)
        standCmd = StandCommand()
        doubleCmd = DoubleCommand(hitCmd, standCmd)
        slot.seatPlayer(player)
        slot.addCards(Card(5,'C'), Card(5, 'H'))
        player.receive_payment(cfg['MINIMUM_BET'])
        slot.promptBet()
        self.assertFalse(doubleCmd.isAvailable(slot), 'testDoubleCommand:testIsAvailable:Double should not be available for player with insufficient money')
        player.receive_payment(cfg['MINIMUM_BET'] *
                               (1 + cfg['DOUBLE_RATIO']))
        slot.promptBet()
        self.assertTrue(doubleCmd.isAvailable(slot), 'testDoubleCommand:testIsAvailable:Double should be availabe for player with sufficient money and unrestricted totals')
        hitCmd.perform(slot)
        player.receive_payment(cfg['MINIMUM_BET'] *
                               (1 + cfg['DOUBLE_RATIO']))
        self.assertFalse(doubleCmd.isAvailable(slot), 'testDoubleCommand:testIsAvailable:Double should not be available beyond first action')
        cfg.mergeFile('cfg/double_totals.ini')
        slot.clearHands()
        slot.addCards(Card(2,'H'), Card(4, 'C'))
        self.assertFalse(doubleCmd.isAvailable(slot), 'testDoubleCommand:testIsAvailable:Double should not be availabe if total not in allowed totals')

        slot.clearHands()
        slot.addCards(Card(5,'H'), Card(4, 'C'))
        self.assertTrue(doubleCmd.isAvailable(slot), 'testDoubleCommand:testIsAvailable:Double should be available when totals match')
        splitCmd = SplitCommand(hitCmd, standCmd)
        player.receive_payment(cfg['MINIMUM_BET'] *
                               (1 + cfg['SPLIT_RATIO']))
        slot.clearHands()
        slot.addCards(Card(5,'C'), Card(5, 'H'))
        splitCmd.perform(slot)
        cfg.mergeFile('cfg/DAS_false.ini')
        self.assertFalse(doubleCmd.isAvailable(slot), 'testDoubleCommand:testIsAvailbe:Double should not be available if player split and DAS is disallowed')

        cfg.reset()
        self.assertTrue(doubleCmd.isAvailable(slot), 'testDoubleCommand:testIsAvailable:Double should be available after split if DAS is allowed')
        slot.clearHands()
        slot.addCards(Card(2,'H'), Card(4, 'C'))
        player.receive_payment(cfg['MINIMUM_BET'] *
                                    (1 + cfg['DOUBLE_RATIO']))
        self.assertTrue(doubleCmd.isAvailable(slot), 'testDoubleCommand:testIsAvailable:Double should be availabe under sufficient funds and appropriate configurations')

if __name__ == '__main__':
    unittest.main()

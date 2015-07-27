####################
#
# testDoubleCommand.py
#
####################

import unittest

from src.Basic.Card          import Card
from src.Basic.Shoe          import Shoe
from src.Logic.DoubleCommand import DoubleCommand
from src.Logic.HitCommand    import HitCommand
from src.Logic.StandCommand  import StandCommand
from src.Logic.SplitCommand  import SplitCommand
from src.Logic.MinBettingStrategy import MinBettingStrategy
from src.Game.TableSlot      import TableSlot
from src.Game.Player         import Player
from src.Utilities.Configuration import Configuration

class testDoubleCommand(unittest.TestCase):
    def setUp(self):
        Configuration.loadConfiguration()
        
    def tearDown(self):
        pass

    def testPerform(self):
        slot = TableSlot()
        player = Player("Test", None, None, MinBettingStrategy())
        slot.seatPlayer(player)
        shoe = Shoe(1,lambda x:x)
        hitCmd = HitCommand(shoe)
        standCmd = StandCommand()
        doubleCmd = DoubleCommand(hitCmd, standCmd)
        player.receive_payment(Configuration.get('MINIMUM_BET') *
                               (1 + Configuration.get('DOUBLE_RATIO')))
        slot.promptBet()
        rc = doubleCmd.perform(slot)
        self.assertEqual(player.stackAmount, 0, 'testDoubleCommand:testPerform:Double should remove amount in pot from player')
        self.assertTrue(rc, 'testDoubleCommand:testPerform:Double should always end hand')
        self.assertEqual(slot.handValue, 2, 'testDoubleCommand:testPerform:Double should add next card in shoe to hand')

    def testIsAvailable(self):
        slot = TableSlot()
        player = Player("Test", None, None, MinBettingStrategy())
        shoe = Shoe(1,lambda x:x)
        hitCmd = HitCommand(shoe)
        standCmd = StandCommand()
        doubleCmd = DoubleCommand(hitCmd, standCmd)
        slot.seatPlayer(player)
        slot.addCards(Card(5,'C'), Card(5, 'H'))
        player.receive_payment(Configuration.get('MINIMUM_BET'))
        slot.promptBet()
        self.assertFalse(doubleCmd.isAvailable(slot), 'testDoubleCommand:testIsAvailable:Double should not be available for player with insufficient money')
        player.receive_payment(Configuration.get('MINIMUM_BET') *
                               (1 + Configuration.get('DOUBLE_RATIO')))
        slot.promptBet()
        Configuration.set('TOTALS_ALLOWED_FOR_DOUBLE', Configuration.UNRESTRICTED)
        self.assertTrue(doubleCmd.isAvailable(slot), 'testDoubleCommand:testIsAvailable:Double should be availabe for player with sufficient money and unrestricted totals')
        hitCmd.perform(slot)
        player.receive_payment(Configuration.get('MINIMUM_BET') *
                               (1 + Configuration.get('DOUBLE_RATIO')))
        self.assertFalse(doubleCmd.isAvailable(slot), 'testDoubleCommand:testIsAvailable:Double should not be available beyond first action')
        Configuration.set('TOTALS_ALLOWED_FOR_DOUBLE', [9, 10, 11])
        slot.clearHands()
        slot.addCards(Card(2,'H'), Card(4, 'C'))
        self.assertFalse(doubleCmd.isAvailable(slot), 'testDoubleCommand:testIsAvailable:Double should not be availabe if total not in allowed totals')
        slot.clearHands()
        slot.addCards(Card(5,'H'), Card(4, 'C'))
        self.assertTrue(doubleCmd.isAvailable(slot), 'testDoubleCommand:testIsAvailable:Double should be available when totals match')
        splitCmd = SplitCommand(hitCmd, standCmd)
        player.receive_payment(Configuration.get('MINIMUM_BET') *
                               (1 + Configuration.get('SPLIT_RATIO')))
        slot.clearHands()
        slot.addCards(Card(5,'C'), Card(5, 'H'))
        splitCmd.perform(slot)
        Configuration.set('DOUBLE_AFTER_SPLIT_ALLOWED', False)
        self.assertFalse(doubleCmd.isAvailable(slot), 'testDoubleCommand:testIsAvailbe:Double should not be available if player split and DAS is disallowed')
        Configuration.set('TOTALS_ALLOWED_FOR_DOUBLE', Configuration.UNRESTRICTED)
        Configuration.set('DOUBLE_AFTER_SPLIT_ALLOWED', True)
        self.assertTrue(doubleCmd.isAvailable(slot), 'testDoubleCommand:testIsAvailable:Double should be available after split if DAS is allowed')
        slot.clearHands()
        slot.addCards(Card(2,'H'), Card(4, 'C'))
        player.receive_payment(Configuration.get('MINIMUM_BET') *
                                    (1 + Configuration.get('DOUBLE_RATIO')))
        Configuration.set('TOTALS_ALLOWED_FOR_DOUBLE', Configuration.UNRESTRICTED)
        self.assertTrue(doubleCmd.isAvailable(slot), 'testDoubleCommand:testIsAvailable:Double should be availabe under sufficient funds and appropriate configurations')

if __name__ == '__main__':
    unittest.main()

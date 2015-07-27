####################
#
# testSplitCommand.py
#
####################

import unittest

from src.Basic.Card          import Card
from src.Basic.Shoe          import Shoe
from src.Basic.BlackjackHand import BlackjackHand
from src.Logic.DoubleCommand import DoubleCommand
from src.Logic.HitCommand    import HitCommand
from src.Logic.StandCommand  import StandCommand
from src.Logic.SplitCommand  import SplitCommand
from src.Logic.MinBettingStrategy import MinBettingStrategy
from src.Game.TableSlot      import TableSlot
from src.Game.Player         import Player
from src.Utilities.Configuration import Configuration

class testSplitCommand(unittest.TestCase):
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
        splitCmd = SplitCommand(hitCmd, standCmd)
        player.receive_payment(Configuration.get('MINIMUM_BET') *
                               (1 + Configuration.get('SPLIT_RATIO')))
        slot.addCards(Card(5,'C'), Card(5,'H'))
        slot.promptBet()
        rc = splitCmd.perform(slot)
        self.assertFalse(rc, 'testSplitCommand:testPerform:Split should not end hand')
        self.assertEqual(player.stackAmount, 0, 'testSplitCommand:testPerform:Split should deduct appropriate amount from player')
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
        player = Player("Test", None, None, MinBettingStrategy())
        slot.seatPlayer(player)
        shoe = Shoe(1,lambda x:x)
        hitCmd = HitCommand(shoe)
        standCmd = StandCommand()
        splitCmd = SplitCommand(hitCmd, standCmd)
        player.receive_payment(Configuration.get('MINIMUM_BET'))
        slot.addCards(Card(5,'C'), Card(6,'C'))
        slot.promptBet()
        self.assertFalse(splitCmd.isAvailable(slot), 'testSplitCommand:testIsAvailable:Split should not be available to insufficiently funded player')
        player.receive_payment(Configuration.get('MINIMUM_BET') *
                               Configuration.get('SPLIT_RATIO'))
        slot.promptBet()
        self.assertFalse(splitCmd.isAvailable(slot), 'testSplitCommand:testIsAvailable:Split should not be avaible to non-pair hand')
        Configuration.set('SPLIT_BY_VALUE', False)
        slot.clearHands()
        slot.addCards(Card(10,'C'), Card('K','C'))
        self.assertFalse(splitCmd.isAvailable(slot), 'testSplitCommand:testIsAvailable:Split should not be available to non rank-paired hand when split by value is disallowed')
        slot.clearHands()
        Configuration.set('SPLIT_BY_VALUE', True)
        slot.addCards(Card(10,'C'), Card('K','C'))
        self.assertTrue(splitCmd.isAvailable(slot), 'testSplitCommand:testIsAvailable:Split should be availabe to non rank-paired hand when split by value is allowed')
        hitCmd.perform(slot)
        self.assertFalse(splitCmd.isAvailable(slot), 'testSplitCommand:testIsAvailable:Split should not be availabe to hand beyond first action')
        Configuration.set('RESPLIT_UP_TO', 0)
        slot.clearHands()
        slot.promptBet()
        slot.addCards(Card(5,'C'), Card(5,'C'))
        self.assertFalse(splitCmd.isAvailable(slot), 'testSplitCommand:testIsAvailable:Split should not be availabe if splitting is disallowed')
        Configuration.set('RESPLIT_UP_TO', Configuration.UNRESTRICTED)
        player.receive_payment(Configuration.get('MINIMUM_BET') *
                               (2 + 2 * Configuration.get('SPLIT_RATIO')))
        slot.promptBet()
        splitCmd.perform(slot)
        slot.clearHands()
        slot.addCards(Card('A','C'), Card('A','H'))
        splitCmd.perform(slot)
        slot.hand.reset()
        slot.hand.addCards(Card('A','C'), Card('A', 'H'))
        Configuration.set('RESPLIT_ACES', True)
        self.assertFalse(splitCmd.isAvailable(slot), 'testSplitCommand:testIsAvailable:Split should not be available if hand is aces from split and resplitting aces is disallowed')
        player.receive_payment(Configuration.get('MINIMUM_BET') *
                               (2 + Configuration.get('SPLIT_RATIO')))
        Configuration.set('RESPLIT_ACES', True)
        self.assertTrue(splitCmd.isAvailable(slot), 'testSplitCommand:testIsAvailable:Split should be available on split aces if resplit aces allowed')

if __name__ == '__main__':
    unittest.main()

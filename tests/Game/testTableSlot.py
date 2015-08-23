####################
#
# testTableSlot.py
#
####################

import unittest

from src.Basic.Card               import Card
from src.Basic.BlackjackHand      import BlackjackHand
from src.Game.Player              import Player
from src.Game.TableSlot           import TableSlot
from src.Logic.BettingStrategy    import BettingStrategy
from src.Logic.MinBettingStrategy import MinBettingStrategy
import src.Utilities.Configuration as config

class testTableSlot(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInit(self):
        slot = TableSlot()
        self.assertEqual(slot.hand.numCards,0, 'testTableSlot:testInit:Slot\'s hand should be empty')
        self.assertTrue(slot.player is None, 'testTableSlot:testInit:Slot\'s player should be initialized to None')

    def testHand(self):
        slot = TableSlot()
        slot.addCards(Card(4,'D'), Card(6,'H'))
        hand = BlackjackHand()
        hand.addCards(Card(4,'D'), Card(6,'H'))
        self.assertEqual(slot.hand, hand, 'testTableSlot:testHand:Hand should return Hand')

    def testHandIsAcePair(self):
        slot = TableSlot()
        slot.addCards(Card('A','H'), Card('A', 'D'))
        self.assertTrue(slot.handIsAcePair, 'testTableSlot:testHandIsAcePair:Pair of aces should return True')
        slot.addCards(Card('A','C'))
        self.assertFalse(slot.handIsAcePair, 'testTableSlot:testHandIsAcePair:Three aces should return False')

    def testFirstAction(self):
        slot = TableSlot()
        slot.addCards(Card(9,'D'), Card(8,'H'))
        self.assertTrue(slot.firstAction, 'testTableSlot:testFirstAction:New hand should be first action')
        slot.addCards(Card(4,'D'))
        self.assertFalse(slot.firstAction, 'testTableSlot:testFirstAction:Hit hand should not be first action')

    def testNumSplits(self):
        slot = TableSlot()
        slot.addCards(Card(9,'D'), Card(8,'H'))
        self.assertEqual(slot.numSplits,0,'testTableSlot:testNumSplits:New hand should have no splits')
        slot = TableSlot()
        player = Player('', None, MinBettingStrategy(), None)
        player.receive_payment(config.get('SPLIT_RATIO'))
        slot.seatPlayer(player)
        slot.addCards(Card(7,'D'), Card(7,'H'))
        slot.splitHand()
        self.assertEqual(slot.numSplits,1,'testTableSlot:testNumSplits:Split hand should have 1 split')
        slot.addCards(Card(7,'C'))
        slot.splitHand()
        self.assertEqual(slot.numSplits,2,'testTableSlot:testNumSplits:Resplit hand should have 2 splits')

    def testHandWasSplit(self):
        slot = TableSlot()
        slot.addCards(Card(9,'D'), Card(8,'H'))
        self.assertFalse(slot.handWasSplit,'testTableSlot:testNumSplits:New hand should not have come from split')
        slot = TableSlot()
        player = Player('', None, MinBettingStrategy(), None)
        player.receive_payment(config.get('SPLIT_RATIO'))
        slot.seatPlayer(player)
        slot.addCards(Card(7,'D'), Card(7,'H'))
        slot.splitHand()
        self.assertTrue(slot.handWasSplit,'testTableSlot:testNumSplits:Split hand should have come from split')
        slot.index += 1
        self.assertTrue(slot.handWasSplit,'testTableSlot:testNumSplits:Split hand should have come from split')
        slot.addCards(Card(7,'C'))
        slot.splitHand()
        self.assertTrue(slot.handWasSplit,'testTableSlot:testNumSplits:Resplit hand should have come from split')

    def testPlayerCanDoubleBet(self):
        pass

    def testIsActive(self):
        player = Player('Tim', None, None, MinBettingStrategy())
        player.receive_payment(1000)
        slot = TableSlot()
        slot.seatPlayer(player)
        slot.promptBet()
        self.assertTrue(slot.isActive,'testTableSlot:testIsActive:Slot with betting player should be active')

        class NoBettingStrategy(BettingStrategy):
            def bet(self, **kwargs):
                return 0

        player = Player('Jack',None, None, NoBettingStrategy())
        slot = TableSlot()
        slot.seatPlayer(player)
        slot.promptBet()
        self.assertFalse(slot.isActive,'testTableSlot:testIsActive:Slot with non-betting player should not be active')
        slot = TableSlot()
        self.assertFalse(slot.isActive,'testTableSlot:testIsActive:Empty slot should not be active')

    def testIsOccupied(self):
        player = Player('John', None, None, None)
        slot = TableSlot()
        self.assertFalse(slot.isOccupied,'testTableSlot:testIsOccupied:Empty slot should not be occupied')
        slot.seatPlayer(player)
        self.assertTrue(slot.isOccupied,'testTableSlot:testIsOccupied:Slot with seated player should be occupied')
        slot.unseatPlayer()
        self.assertFalse(slot.isOccupied,'testTableSlot:testIsOccupied:Slot with unseated player should not be occupied')

if __name__ == '__main__':
    unittest.main()

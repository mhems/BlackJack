import unittest

from cards import (Card, Shoe)
from commands import (HitCommand,
                      SurrenderCommand)
from config import cfg
from game import Player
from policies import MinBettingPolicy
from table import TableSlot

class testSurrenderCommand(unittest.TestCase):
    def setUp(self):
        self.surrenderCmd = SurrenderCommand()
        self.slot = TableSlot()

    def tearDown(self):
        pass

    def testPerform(self):
        rc = self.surrenderCmd.perform(self.slot)
        self.assertTrue(self.slot.surrendered, 'testSurrenderCommand:testPerform:Surrender should be reflected in the tableslot')
        self.assertTrue(rc, 'testSurrenderCommand:testPerform:Surrender should end player\'s turn')

    def testIsAvailable(self):
        player = Player("Test", None, None, MinBettingPolicy())
        player.receive_payment(cfg['MINIMUM_BET'])
        self.slot.seatPlayer(player)
        self.slot.addCards(Card('A','H'), Card(6,'D'))
        cfg.mergeFile('cfg/no_surrender.ini')
        self.assertFalse(self.surrenderCmd.isAvailable(self.slot), 'testSurrenderCommand:testIsAvailable:Surrender should not be available if disallowed')

        cfg.reset()
        self.assertTrue(self.surrenderCmd.isAvailable(self.slot), 'testSurrenderCommand:testIsAvailable:Surrender should be available if allowed')

        HitCommand(Shoe(2, lambda x:x)).perform(self.slot)
        self.assertFalse(self.surrenderCmd.isAvailable(self.slot), 'testSurrenderCommand:testIsAvailable:Surrender should not be available after first action')

if __name__ == '__main__':
    unittest.main()

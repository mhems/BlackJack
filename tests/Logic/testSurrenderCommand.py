import unittest

from src.Basic.Card import Card
from src.Basic.Shoe import Shoe
from src.Logic.Command import (HitCommand,
                               SurrenderCommand)
from src.Logic.BettingStrategy import MinBettingStrategy
from src.Game.TableSlot import TableSlot
from src.Game.Player import Player
import src.Utilities.Configuration as config

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
        player = Player("Test", None, None, MinBettingStrategy())
        player.receive_payment(config.get('MINIMUM_BET'))
        self.slot.seatPlayer(player)
        self.slot.addCards(Card('A','H'), Card(6,'D'))
        config.loadConfiguration('tests/Logic/test_files/no_surrender.ini')
        self.assertFalse(self.surrenderCmd.isAvailable(self.slot), 'testSurrenderCommand:testIsAvailable:Surrender should not be available if disallowed')

        config.loadDefaultConfiguration()
        self.assertTrue(self.surrenderCmd.isAvailable(self.slot), 'testSurrenderCommand:testIsAvailable:Surrender should be available if allowed')

        HitCommand(Shoe(2, lambda x:x)).perform(self.slot)
        self.assertFalse(self.surrenderCmd.isAvailable(self.slot), 'testSurrenderCommand:testIsAvailable:Surrender should not be available after first action')

if __name__ == '__main__':
    unittest.main()

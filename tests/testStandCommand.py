import unittest

from cards import Shoe
from commands import StandCommand
from game import Player
from table import TableSlot

class testStandCommand(unittest.TestCase):
    def setUp(self):
        self.slot = TableSlot()
        player = Player("Test", None, None, None)
        self.slot.seatPlayer(player)

    def tearDown(self):
        pass

    def testPerform(self):
        standCmd = StandCommand()
        hand = self.slot.hand
        rc = standCmd.perform(self.slot)
        self.assertEqual(hand, self.slot.hand, 'testStandCommand:testPerform:Stand should not alter player\'s hand')
        self.assertTrue(rc,'testStandCommand:testPerform:Stand should always end player\'s turn')

    def testIsAvailable(self):
        standCmd = StandCommand()
        self.assertTrue(standCmd.isAvailable(self.slot), 'testStandCommand:testPerform:Stand should always be available')

if __name__ == '__main__':
    unittest.main()

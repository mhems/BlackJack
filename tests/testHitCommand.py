import unittest

from src.commands import HitCommand
from src.cards import Shoe
from src.TableSlot import TableSlot
from src.Player import Player

class testHitCommand(unittest.TestCase):
    def setUp(self):
        self.slot = TableSlot()
        player = Player("Test", None, None, None)
        self.slot.seatPlayer(player)
        self.shoe = Shoe(1, lambda x: x)

    def tearDown(self):
        pass

    def testPerform(self):
        hitCmd = HitCommand(self.shoe)
        rc = hitCmd.perform(self.slot)
        self.assertEqual(self.slot.hand.value,2,'testHitCommand:testPeform:Hit should add next card in shoe to slot player\'s hand')
        self.assertFalse(rc,'testHitCommand:testPerform:Hit should never directly end hand')
        hitCmd.perform(self.slot)
        self.assertEqual(self.slot.hand.value,4,'testHitCommand:testPeform:Hit should add next card in shoe to slot player\'s hand')

    def testIsAvailable(self):
        hitCmd = HitCommand(self.shoe)
        self.assertTrue(hitCmd.isAvailable(self.slot), 'testHitCommand:testIsAvailable"Hit should always be available')

if __name__ == '__main__':
    unittest.main()

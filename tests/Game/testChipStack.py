####################
#
# testChipStack.py
#
####################

import unittest

from src.Game.Bank      import InsufficientFundsError
from src.Game.ChipStack import ChipStack

class testChipStack(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInit(self):
        stack = ChipStack()
        self.assertEqual(stack.amount,0,'testChipStack:testInit:ChipStack should be zero initialized')

    def testWithdraw(self):
        stack = ChipStack()
        stack.deposit(50)
        stack.withdraw(50)
        self.assertEqual(stack.amount,0,'testChipStack:testWithdraw:Full withdrawal should leave no funds')
        stack.deposit(100)
        stack.withdraw(75)
        self.assertEqual(stack.amount,25,'testChipStack:testWithdraw:Withdrawal should leave appropriate funds')
        with self.assertRaises(InsufficientFundsError):
            stack.withdraw(50)

    def testDeposit(self):
        stack = ChipStack()
        stack.deposit(100)
        self.assertEqual(stack.amount,100,'testChipStack:testDeposit:Deposit should deposit money')
        stack.deposit(50)
        self.assertEqual(stack.amount,150,'testChipStack:testDeposit:Deposit should deposit money')

if __name__ == '__main__':
    unittest.main()

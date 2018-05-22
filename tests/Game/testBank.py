import unittest

from src.Game.Bank import InsufficientFundsError
from src.Game.Bank import Bank

class testBank(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInit(self):
        stack = Bank()
        self.assertEqual(stack.amount,0,'testBank:testInit:Bank should be zero initialized')

    def testWithdraw(self):
        stack = Bank()
        stack.deposit(50)
        stack.withdraw(50)
        self.assertEqual(stack.amount,0,'testBank:testWithdraw:Full withdrawal should leave no funds')
        stack.deposit(100)
        stack.withdraw(75)
        self.assertEqual(stack.amount,25,'testBank:testWithdraw:Withdrawal should leave appropriate funds')
        with self.assertRaises(InsufficientFundsError):
            stack.withdraw(50)

    def testDeposit(self):
        stack = Bank()
        stack.deposit(100)
        self.assertEqual(stack.amount,100,'testBank:testDeposit:Deposit should deposit money')
        stack.deposit(50)
        self.assertEqual(stack.amount,150,'testBank:testDeposit:Deposit should deposit money')

if __name__ == '__main__':
    unittest.main()

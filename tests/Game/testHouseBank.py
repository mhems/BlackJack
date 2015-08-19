####################
#
# testHouseBank.py
#
####################

import unittest

from src.Game.HouseBank import HouseBank

class testHouseBank(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInit(self):
        house = HouseBank()
        self.assertEqual(house.amount,0,'testHouseBank:testInit:HouseBank should be zero initialized')

    def testWithdraw(self):
        house = HouseBank()
        house.deposit(50)
        house.withdraw(50)
        self.assertEqual(house.amount,0,'testHouseBank:testWithdraw:Full withdrawal should leave no funds')
        house.deposit(100)
        house.withdraw(75)
        self.assertEqual(house.amount,25,'testHouseBank:testWithdraw:Withdraw should leave appropriat funds')
        house.withdraw(50)
        self.assertEqual(house.amount,-25,'testHouseBank:testWithdraw:Overwithdraw should leave negative amount')

    def deposit(self):
        house = HouseBank()
        house.deposit(100)
        self.assertEqual(house.amount,100,'testHouseBank:testDeposit:Deposit should deposit money')
        house.deposit(50)
        self.assertEqual(house.amount,100,'testHouseBank:testDeposit:Deposit should deposit money')

if __name__ == '__main__':
    unittest.main()

####################
#
# testEnum.py
#
####################

import unittest

from src.Utilities.Enum import Enum

class testEnum(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEQ(self):
        a = Enum()
        b = Enum()
        c = Enum()
        d = a
        self.assertFalse(a == b,'testEnum:testEQ:Non-identical Enums should not be equal')
        self.assertFalse(a == c,'testEnum:testEQ:Non-identical Enums should not be equal')
        self.assertFalse(b == c,'testEnum:testEQ:Non-identical Enums should not be equal')
        self.assertTrue( a == d,'testEnum:testEQ:Identical Enums should be equal')

    def testNE(self):
        a = Enum()
        b = Enum()
        c = Enum()
        d = a
        self.assertTrue( a != b,'testEnum:testNE:Non-identical Enums should not be equal')
        self.assertTrue( a != c,'testEnum:testNE:Non-identical Enums should not be equal')
        self.assertTrue( b != c,'testEnum:testNE:Non-identical Enums should not be equal')
        self.assertFalse(a != d,'testEnum:testNE:Identical Enums should be equal')

if __name__ == '__main__':
    unittest.main()

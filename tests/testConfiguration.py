import unittest

from src.config import *

class testConfiguration(unittest.TestCase):

    prefix = 'tests/test_files/'

    def setUp(self):
        loadDefaultConfiguration()
        self.checkBadSemantics = self.assertIsRaised(SemanticConfigError)
        self.checkBadValue     = self.assertIsRaised(ValueError)

    def tearDown(self):
        pass

    def assertIsRaised(self, error):
        def __check(filename):
            self.assertRaises(error, loadConfiguration, self.prefix + filename)
        return __check

    def testNegPosInt(self):
        self.checkBadSemantics('neg_pos_int.ini')

    def testFloatInt(self):
        self.checkBadValue('float_int.ini')

    def testZeroPos(self):
        self.checkBadSemantics('zero_pos.ini')

    def testBadBool(self):
        self.checkBadValue('bad_bool.ini')

    def testOverBurn(self):
        self.checkBadSemantics('over_burn.ini')

    def testOverCut(self):
        self.checkBadSemantics('over_cut.ini')

    def testBadRatio(self):
        self.checkBadSemantics('bad_ratio.ini')

    def testNegRatio(self):
        self.checkBadSemantics('neg_ratio.ini')

    def testImproperRatio(self):
        self.checkBadSemantics('improper_ratio.ini')

    def testBadRange(self):
        pass

    def testEmptyRange(self):
        pass

    def testMalRange(self):
        pass

    def testBadMaxBet(self):
        self.checkBadSemantics('bad_max_bet.ini')

if __name__ == '__main__':
    unittest.main()

####################
#
# testDeclineInsurancePolicy.py
#
####################

import unittest

from src.Logic.DeclineInsurancePolicy import DeclineInsurancePolicy

class testDeclineInsurancePolicy(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInsure(self):
        policy = DeclineInsurancePolicy()
        self.assertFalse(policy.insure(None), 'testDeclineInsurancePolicy:testInsure:Decline should always decline')

if __name__ == '__main__':
    unittest.main()

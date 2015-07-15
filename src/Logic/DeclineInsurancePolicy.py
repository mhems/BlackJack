####################
#
# DeclineInsurancePolicy.py
#
####################

from src.Logic.InsurancePolicy import InsurancePolicy

class DeclineInsurancePolicy(InsurancePolicy):
    """Policy that always declines insurance offers"""

    def insure(self, hand, **kwargs):
        """Always returns False"""
        return False

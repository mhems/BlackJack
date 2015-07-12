####################
#
# HumanInputInsurancePolicy.py
#
####################

from src.Logic.InsurancePolicy import InsurancePolicy

class HumanInputInsurancePolicy(InsurancePolicy):
    """Policy that prompts for whether to accept insurance offer"""

    def accept_insurance(self, hand, **kwargs):
        """Returns True iff input indicates wish to accept insurance"""
        response = 'unitialized'
        while response[0].lower() not in ['y', 'n']:
            response = input('Accept insurance? (Yes/No)')
        return response[0].lower() == 'y'

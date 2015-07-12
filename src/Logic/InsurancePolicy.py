####################
#
# InsurancePolicy.py
#
####################

from abc import ABCMeta, abstractmethod

class InsurancePolicy(metaclass=ABCMeta):
    """Base Class for insurance policies on when to accept insurance"""

    @abstractmethod
    def accept_insurance(self, hand, **kwargs):
        """Return True if player accepts insurance offer"""
        raise NotImplementedError(
            'InsurancePolicy implementations must implement the accept_insurance method')

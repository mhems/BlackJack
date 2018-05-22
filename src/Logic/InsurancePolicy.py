from abc import ABCMeta, abstractmethod

class InsurancePolicy(metaclass=ABCMeta):
    """Base Class for insurance policies on when to accept insurance"""

    @abstractmethod
    def insure(self, hand, **kwargs):
        """Return True if player accepts insurance offer"""
        raise NotImplementedError(
            'InsurancePolicy implementations must implement the insure method')

class DeclineInsurancePolicy(InsurancePolicy):
    """Policy that always declines insurance offers"""

    def insure(self, hand, **kwargs):
        """Always returns False"""
        return False

class HumanInputInsurancePolicy(InsurancePolicy):
    """Policy that prompts for whether to accept insurance offer"""

    def insure(self, hand, **kwargs):
        """Returns True iff input indicates wish to insure"""
        response = 'uninitialized'
        while response[0].lower() not in ['y', 'n']:
            response = input('Your hand (%s) has value %d, '
                             'Take insurance? (Yes/No)' %
                             (str(hand), hand.value))
        return response[0].lower() == 'y'

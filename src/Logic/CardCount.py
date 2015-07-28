####################
#
# CardCount.py
#
####################

from src.Basic.Shoe import Shoe

class CardCount():
    """Pluggable mechanism for card counting"""

    def __init__(self):
        """Initializes members"""
        self.__count = 0

    @property
    def runningCount(self):
        """Returns current running count"""
        return self.__count

    def update(self, card):
        """Updates count based on card"""
        if card is None:
            self.__count = 0
        else:
            self.__count += self.computeValue(card)

    @classmethod
    def computeValue(cls, card):
        """Computes value to add to count based on card and method"""
        return cls.ranking[card.value - 2]
    
class HiLoCount(CardCount):
    """Uses the Hi-Lo counting system"""

    ranking = [1, 1, 1, 1, 1, 0, 0, 0, -1, -1]

class HiOptOneCount(CardCount):
    """Uses the Hi-Opt I counting system"""

    ranking = [0, 1, 1, 1, 1, 0, 0, 0, -1, 0]

class HiOptTwoCount(CardCount):
    """Uses the Hi-Opt II counting system"""

    ranking = [1, 1, 2, 2, 1, 1, 0, 0, -2, 0]

class KOCount(CardCount):
    """Uses the KO counting system"""

    ranking = [1, 1, 1, 1, 1, 1, 0, 0, -1, -1]

class OmegaTwoCount(CardCount):
    """Uses the Omega II counting system"""

    ranking = [1, 1, 2, 2, 2, 1, 0, -1, -2, 0]

class RedSevenCount(CardCount):
    """Uses the Red 7 counting system"""

    ranking = [1, 1, 1, 1, 1, 0.5, 0, 0, -1, -1]

class ZenCount(CardCount):
    """Uses the Zen Count counting system"""

    ranking = [1, 1, 2, 2, 2, 1, 0, 0, -2, -1]

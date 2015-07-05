####################
#
# Enum.py
#
####################

class Enum():
    """Mechanism for enumerations, i.e. trivially wrapped ints"""

    __count = 0
    
    def __init__(self):
        """Wraps unique integer"""
        self.__value = Enum.__count
        Enum.__count += 1

    def __eq__(self, other):
        """Returns True iff enum is same integer"""
        return self.__value == other.__value

    def __ne__(self, other):
        """Returns True iff enum and other are not the same integer"""
        return not self == other

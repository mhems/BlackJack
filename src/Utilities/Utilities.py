####################
#
# Utilities.py
#
####################

from sys import stderr
from sys import exit

class Enum:
    """Provides mechanism for 'enum' object"""

    __counter = 0

    def __init__(self):
        self.value = Enum.__counter
        Enum.__counter += 1

    def __eq__(self, other):
        try:
            return self.value == other.value
        except:
            return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.value)

class Utilities:
    """Provides general utilities such as centralized error handling"""

    numErrors = 0
    __count   = 1000

    @staticmethod
    def createEnum():
        """Return unique 'enum'"""
        return Enum()
    
    @staticmethod
    def error(msg):
        stderr.write(msg)
        stderr.write('\n')
        Utilities.numErrors += 1

    @staticmethod
    def fatalError(msg):
        stderr.write(msg)
        stderr.write('\n')
        exit(1)

    @staticmethod
    def printBanner(msg):
        """Prints msg in ASCII banner style"""
        bookend = '+%s+' % ('-' * (len(msg) + 2 * 1))
        print(bookend)
        print('| %s |' % msg)
        print(bookend)

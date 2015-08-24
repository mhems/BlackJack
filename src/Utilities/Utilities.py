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

"""Provides general utilities such as centralized error handling"""

numErrors = 0

def error(msg):
    stderr.write(msg)
    stderr.write('\n')
    Utilities.numErrors += 1

def fatalError(msg):
    stderr.write(msg)
    stderr.write('\n')
    exit(1)

def printBanner(msg):
    """Prints msg in ASCII banner style"""
    bookend = '+%s+' % ('-' * (len(msg) + 2 * 1))
    print(bookend)
    print('| %s |' % msg)
    print(bookend)

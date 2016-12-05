####################
#
# Utilities.py
#
####################

from sys import (platform, stderr, exit)

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

    def __str__(self):
        return str(self.value)

"""Provides general utilities such as centralized error handling"""

LINE_END = '\r\n' if 'win' in platform.lower() else '\n'
numErrors = 0

def warn(msg):
    stderr.write(msg)
    stderr.write(LINE_END)

def error(msg):
    stderr.write(msg)
    stderr.write(LINE_END)
    Utilities.numErrors += 1

def fatalError(msg):
    stderr.write(msg)
    stderr.write(LINE_END)
    exit(1)

def printBanner(msg):
    """Prints msg in ASCII banner style"""
    bookend = '+%s+' % ('-' * (len(msg) + 2 * 1))
    print(bookend)
    print('| %s |' % msg)
    print(bookend)

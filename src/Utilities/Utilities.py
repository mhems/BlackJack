####################
#
# Utilities.py
#
####################

from sys import stderr
from sys import exit

class Utilities:
    """Provides general utilities such as centralized error handling"""

    numErrors = 0
    __count   = 1000

    @staticmethod
    def uniqueNumber():
        """Return previously unseen number"""
        c = Utilities.__count
        Utilities.__count += 1
        return c
    
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

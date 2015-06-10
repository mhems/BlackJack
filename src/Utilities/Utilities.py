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

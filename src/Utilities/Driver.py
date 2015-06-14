####################
#
# Driver.py
#
####################

import os

"""Drives program execution"""

if __name__ == '__main__':
    # ugly hack to ensure imports work
    abspath = os.path.abspath(__file__)
    os.environ['PYTHONPATH'] += ':' + abspath[:len(abspath)-len(__file__)]

    # parse command line arguments
    # establish all parameters

    """
blackjack
    -h (--help) : Display usage information
    -f (--file) : Specify config file to use
    

    """

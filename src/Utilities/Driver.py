####################
#
# Driver.py
#
####################

import os

if __name__ == '__main__':
    # ugly hack to insure imports work
    abspath = os.path.abspath(__file__)
    os.environ['PYTHONPATH'] += ':' + abspath[:len(abspath)-len(__file__)]

    # parse command line arguments
    # establish all parameters

####################
#
# blackjack.py
#
####################

import os
import argparse

"""Drives program execution"""

def parseCommandLine():
    """Parses command line to establish configurations"""
    """Return True upon success"""
    parser = argparse.ArgumentParser(description='Blackjack Game Suit')
    parser.add_argument('-cfg', '--config_file',
                        dest    = 'config_file_name',
                        default = 'config.ini',
                        metavar = 'CONFIG_FILE',
                        help    = 'the location of the configuration file')
    return parser.parse_args()

if __name__ == '__main__':
    # ugly hack to ensure imports work
    abspath = os.path.abspath(__file__)
#    os.environ['PYTHONPATH'] += ':' + abspath[:len(abspath)-len(__file__)]

    nspace = parseCommandLine()

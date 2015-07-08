####################
#
# blackjack.py
#
####################

import os
import argparse

from src.Game.Player import Player
from src.Game.Table  import Table
from src.Logic.HumanInputPolicy   import HumanInputPolicy
from src.Logic.MinBettingStrategy import MinBettingStrategy
from src.Utilities.Configuration  import Configuration

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

    Configuration.loadConfiguration()
    
    player = Player("ME", HumanInputPolicy(), MinBettingStrategy())
    player.receive_payment(100)
    table  = Table()
    table.register_player(player)
    table.play()

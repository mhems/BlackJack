####################
#
# blackjack.py
#
####################

import signal
import sys
import os
import argparse

from src.Game.Player import Player
from src.Game.Table  import Table
from src.Game.Bank   import InsufficientFundsError
from src.Logic.HumanInputPolicy          import HumanInputPolicy
from src.Logic.BasicStrategyPolicy       import BasicStrategyPolicy
from src.Logic.FeedbackDecisionPolicy    import FeedbackDecisionPolicy
from src.Logic.HumanInputInsurancePolicy import HumanInputInsurancePolicy
from src.Logic.DeclineInsurancePolicy    import DeclineInsurancePolicy
from src.Logic.MinBettingStrategy import MinBettingStrategy
from src.Utilities.Configuration  import loadConfiguration
from src.Utilities.Utilities      import LINE_END

"""Drives program execution"""

def parseCommandLine():
    """Parses command line to establish configurations"""
    """Return True upon success"""
    parser = argparse.ArgumentParser(description='Blackjack Game Suit')
    parser.add_argument('-cfg', '--config_file',
                        dest    = 'config_file_name',
                        metavar = 'CONFIG_FILE',
                        help    = 'the location of the configuration file')
    return parser.parse_args()

def handler(signum, frame):
    """Exits"""
    print("Exiting...")
    sys.exit(0)

if __name__ == '__main__':
    # establish interrupt handlers
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT,  handler)

    nspace = parseCommandLine()

    loadConfiguration(nspace.config_file_name)

    hip1   = HumanInputPolicy()
    strat1 = BasicStrategyPolicy('tests/Logic/test_files/three_chart.txt')
    player = Player("Matt",
                    FeedbackDecisionPolicy(hip1, strat1),
                    HumanInputInsurancePolicy(),
                    MinBettingStrategy())
    player.receive_payment(100)
    player2 = Player("Billy Batch",
                     strat1,
                     DeclineInsurancePolicy(),
                     MinBettingStrategy())
    player2.receive_payment(100)
    table = Table()
    # table.register_player(player)
    table.register_player(player2)
    try:
        while True:
            table.play()
            print(LINE_END)
    except InsufficientFundsError as e:
        print(e)

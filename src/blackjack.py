"""Drives program execution"""

import argparse
import signal
import sys

from config import (cfg, SemanticConfigError)
from game import (InsufficientFundsError, Player)
from policies import (BasicStrategyPolicy,
                      CardCount,
                      DeclineInsurancePolicy,
                      FeedbackDecisionPolicy,
                      HumanInputPolicy,
                      MinBettingPolicy)
from table import Table

def parseCommandLine():
    """Parses command line to establish configurations.
    Returns True upon success"""
    parser = argparse.ArgumentParser(description='Blackjack Game Suit')
    parser.add_argument('-cfg', '--config_file',
                        default = 'cfg/default_config.ini',
                        dest    = 'config_file_name',
                        metavar = 'CONFIG_FILE',
                        help    = 'the location of the configuration file')
    return parser.parse_args()

if __name__ == '__main__':
    nspace = parseCommandLine()

    try:
        cfg.mergeFile(nspace.config_file_name)
    except SemanticConfigError as e:
        print(e)

    hip1 = HumanInputPolicy()
    strat = BasicStrategyPolicy('cfg/three_chart.txt')
    strat1 = FeedbackDecisionPolicy(hip1, strat)
    player = Player("Matt",
                    strat1,
                    DeclineInsurancePolicy(),
                    MinBettingPolicy())
    player.receive_payment(10000)

    player2 = Player("Billy Batch",
                     strat,
                     DeclineInsurancePolicy(),
                     MinBettingPolicy())
    player2.receive_payment(1000)

    table = Table()
    table.register_player(player)
    nRounds = 0
    counter = CardCount('HiLoCount')
    table.shoe.registerObserver(counter)

    def handler(_signum, _frame):
        """Handles Ctrl+C signals"""
        print()
        print(str(nRounds) + ' rounds played')
        print(str(strat1.num_wrong) + ' hands played incorrectly')
        sys.exit(0)

    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT,  handler)

    try:
        while True:
            table.play()
            print('Count is ' + str(counter.count))
            print()
            nRounds += 1
    except InsufficientFundsError as e:
        print(e)
    handler(None, None)

import signal
import sys
import os
import argparse

from src.Game.Player import Player
from src.Game.Table  import Table
from src.Game.Bank   import InsufficientFundsError
from src.Logic.DecisionPolicy          import HumanInputPolicy
from src.Logic.DecisionPolicy            import BasicStrategyPolicy
from src.Logic.DecisionPolicy    import FeedbackDecisionPolicy
from src.Logic.InsurancePolicy import HumanInputInsurancePolicy
from src.Logic.InsurancePolicy    import DeclineInsurancePolicy
from src.Logic.BettingStrategy import MinBettingStrategy
from src.Logic.CardCount          import HiLoCount
from src.Utilities.Configuration  import loadConfiguration
from src.Utilities.Utilities      import LINE_END

"""Drives program execution"""

def parseCommandLine():
    """Parses command line to establish configurations"""
    """Return True upon success"""
    parser = argparse.ArgumentParser(description='Blackjack Game Suit')
    parser.add_argument('-cfg', '--config_file',
                        default = 'src/Utilities/default_config.ini',
                        dest    = 'config_file_name',
                        metavar = 'CONFIG_FILE',
                        help    = 'the location of the configuration file')
    return parser.parse_args()

if __name__ == '__main__':

    nspace = parseCommandLine()

    try:
        loadConfiguration(nspace.config_file_name)
    except SemanticConfigError as e:
        print(e)

    hip1   = HumanInputPolicy()
    strat1 = BasicStrategyPolicy('tests/Logic/test_files/three_chart.txt')
    strat1 = FeedbackDecisionPolicy(hip1, strat1)
    player = Player("Matt",
                    strat1,
                    DeclineInsurancePolicy(),
                    MinBettingStrategy())
    player.receive_payment(10000)

    player2 = Player("Billy Batch",
                     strat1,
                     DeclineInsurancePolicy(),
                     MinBettingStrategy())
    player2.receive_payment(1000)

    table = Table()
    table.register_player(player)
    nRounds = 0
    counter = HiLoCount()
    table.shoe.registerObserver(counter)

    def handler(_signum, _frame):
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
            print(LINE_END)
            nRounds += 1
    except InsufficientFundsError as e:
        print(e)
    handler(None, None)

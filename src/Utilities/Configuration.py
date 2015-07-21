####################
#
# Configuration.py
#
####################

from configparser import ConfigParser
import re

from src.Basic.Card          import Card
from src.Utilities.Utilities import Utilities

# Make silent parsing errors notify user

class InvalidOptionError(KeyError):
    """Represents error for unknown configuration option"""
    pass

class Configuration:
    """Provides handling and access of configuration files"""
    
    UNRESTRICTED = Utilities.uniqueNumber()
    
    __configuration = {
        # general
        # > 0
        'BLACKJACK_VALUE'                : 21,
        # > 0
        'NUM_DECKS'                      : 6,
        # True | False
        'PUSH_ON_BLACKJACK'              : True,
        # > 0 => index from shoe front
        # < 0 => index from shoe rear
        'CUT_INDEX'                      : -26,
        # > 0 and < number cards in shoe
        'NUM_CARDS_BURN_ON_SHUFFLE'      : 1,
        
        # payout_ratio
        # ratios must be positive floats or fractions
        'PAYOUT_RATIO'                   : 1,
        'BLACKJACK_PAYOUT_RATIO'         : 1.5,
        'INSURANCE_PAYOUT_RATIO'         : 2,

        # dealer
        # True | False
        'DEALER_HITS_ON_SOFT_17'         : True,
        # True | False
        'DEALER_CHECKS_FOR_BLACKJACK'    : True,
        
        # double
        # True | False
        'DOUBLE_AFTER_SPLIT_ALLOWED'     : True,
        # must be * or comma separated list of card ranks
        'TOTALS_ALLOWED_FOR_DOUBLE'      : '*',
        # must be positive float or fraction
        'DOUBLE_RATIO'                   : 1,

        # split
        # True | False
        'SPLIT_BY_VALUE'                 : True,
        # > 0 or * to denote unlimited
        'RESPLIT_UP_TO'                  : 4,
        # True | False
        'RESPLIT_ACES'                   : True,
        # True | False
        'HIT_SPLIT_ACES'                 : False,
        # must be positive float or fraction
        'SPLIT_RATIO'                    : 1,

        # surrender
        # True | False
        'LATE_SURRENDER'                 : True,
        # must be float or fraction between 0 and 1 inclusive
        'LATE_SURRENDER_RATIO'           : 0.5,
        # True | False
        'EARLY_SURRENDER'                : False,

        # insurance
        # True | False
        'OFFER_INSURANCE'                : True,
        # must be float or fraction between 0 and 1 inclusive
        'INSURANCE_RATIO'                : 0.5,
        
        # game
        # > 0
        'MINIMUM_BET'                    : 15,
        # >= MINIMUM_BET
        'MAXIMUM_BET'                    : 10000,

        # preferences
        # True | False
        'WINNINGS_REMAIN_IN_POT'         : False
    }

    @staticmethod
    def loadConfiguration():
        """Loads configuration data"""
        res = None #Configuration.parseConfigFile(command_line_filename)
        if res:
            Configuration.__assign(res)
        else:
            res = Configuration.parseConfigFile('config.ini')
            if res:
                Configuration.__assign(res)
        # override any options with present command line flags

        # check semantics
        blackjack = Configuration.__configuration['BLACKJACK_VALUE']
        if blackjack < 0:
            Utilities.error('BLACKJACK_VALUE: (%d) Expected number to be positive' % blackjack)
        num_decks = Configuration.__configuration['NUM_DECKS']
        if num_decks < 1:
            Utilities.error('NUM_DECKS: (%d) Expected number to be at least 1' % num_decks)
        num_cards = Configuration.__configuration['NUM_DECKS'] * Card.NUM_CARDS_PER_DECK
        cut_index = Configuration.__configuration['CUT_INDEX']
        if abs(cut_index) > num_cards:
            Utilities.error('CUT_INDEX: (%d) Cut index cannot be greater than number of cards in shoe (%d)' % (cut_index, num_cards))
        num_burn = Configuration.__configuration['NUM_CARDS_BURN_ON_SHUFFLE']
        if num_burn < 0:
            Utilities.error('NUM_CARDS_BURN_ON_SHUFFLE: (%d) Number of cards to burn after shuffle must be positive' % num_burn) 
        if num_burn > num_cards:
            Utilities.error('NUM_CARDS_BURN_ON_SHUFFLE: (%d) Number of cards to burn after shuffle must be at most the number of cards in the deck (%d)' % (num_burn, num_cards))
        Configuration.__checkRatio('PAYOUT_RATIO')
        Configuration.__checkRatio('BLACKJACK_PAYOUT_RATIO')
        Configuration.__checkRatio('INSURANCE_PAYOUT_RATIO')
        Configuration.__checkCardRange('TOTALS_ALLOWED_FOR_DOUBLE')
        Configuration.__checkRatio('DOUBLE_RATIO')
        resplit_num = Configuration.__configuration['RESPLIT_UP_TO']
        if resplit_num == '*':
            Configuration.__configuration['RESPLIT_UP_TO'] = Configuration.UNRESTRICTED
        elif not re.match('0|[1-9][0-9]*', str(resplit_num)):
            Utilities.error('RESPLIT_UP_TO: (%d) Number of times to resplit must be non-negative integer' % resplit_num)
        Configuration.__checkRatio('SPLIT_RATIO')
        Configuration.__checkRatio('LATE_SURRENDER_RATIO', False)
        Configuration.__checkRatio('INSURANCE_RATIO', False)
        min_bet = Configuration.__configuration['MINIMUM_BET']
        if min_bet <= 0:
            Utilities.error('MINIMUM BET: (%d) Minimum amount to bet must be positive' % min_bet);
        max_bet = Configuration.__configuration['MAXIMUM_BET']
        if max_bet <= 0 or max_bet < min_bet:
            Utilities.error('MAXIMUM BET: (%d) Maximum amount to bet must be positive number no less than minimum bet amount (%d)' % (max_bet, min_bet))

        if Utilities.numErrors > 0:
            Utilities.fatalError('Fatal semantic error in configuration options, exiting now')

    @staticmethod
    def __checkRatio(flagname, allowImproper=True):
        """Semantic check of options with ratio values"""
        value = Configuration.__configuration[flagname]
        ratio = None
        try:
            ratio = float(value)
            if ratio < 0:
                Utilities.error('%s: (%s) Ratio must be positive' % (flagname, ratio))
        except ValueError:
            match = re.match('\+?([1-9][0-9]*)/([1-9][0-9]*)', value)
            if match:
                ratio = float(int(match.group(1))/int(match.group(2)))
            else:
                Utilities.error(
                    '%s: (%s) Ratio must be either a decimal or fraction' %
                    (flagname, value) )
        if ratio:
            if not allowImproper and ratio > 1.0:
                Utilities.error(
                    '%s: (%s) Ratio must be between 0 and 1, inclusive' %
                    (flagname, ratio))
            else:
                Configuration.__configuration[flagname] = ratio

    @staticmethod
    def __checkCardRange(flagname):
        """Semantic check of options with range values"""
        value = Configuration.__configuration[flagname]
        if value == '*':
            Configuration.__configuration[flagname] = Configuration.UNRESTRICTED
        else:
            ls = list(set(re.findall('10|J|Q|K|A|[2-9]', value, re.I)))
            for idx, elem in enumerate(ls):
                if re.match('[1-9][0-9]*', elem):
                    ls[idx] = int(elem)
            Configuration.__configuration[flagname] = ls
            
    @staticmethod
    def __assign(conf):
        """Assigns values from configuration file into dictionary"""
        Configuration.__configuration['BLACKJACK_VALUE']               = conf.getint('general','BLACKJACK_VALUE')
        Configuration.__configuration['NUM_DECKS']                     = conf.getint('general','NUM_DECKS')
        Configuration.__configuration['PUSH_ON_BLACKJACK']             = conf.getboolean('general','PUSH_ON_BLACKJACK')
        Configuration.__configuration['CUT_INDEX']                     = conf.getint('general','CUT_INDEX')
        Configuration.__configuration['NUM_CARDS_BURN_ON_SHUFFLE']     = conf.getint('general','NUM_CARDS_BURN_ON_SHUFFLE')
        Configuration.__configuration['PAYOUT_RATIO']                  = conf.get('payout_ratio','PAYOUT_RATIO')
        Configuration.__configuration['BLACKJACK_PAYOUT_RATIO']        = conf.get('payout_ratio','BLACKJACK_PAYOUT_RATIO')
        Configuration.__configuration['INSURANCE_PAYOUT_RATIO']        = conf.get('payout_ratio','INSURANCE_PAYOUT_RATIO')
        Configuration.__configuration['DEALER_HITS_ON_SOFT_17']        = conf.getboolean('dealer','DEALER_HITS_ON_SOFT_17')
        Configuration.__configuration['DEALER_CHECKS_FOR_BLACKJACK']   = conf.getboolean('dealer','DEALER_CHECKS_FOR_BLACKJACK')
        Configuration.__configuration['DOUBLE_AFTER_SPLIT_ALLOWED']    = conf.getboolean('double','DOUBLE_AFTER_SPLIT_ALLOWED')
        Configuration.__configuration['TOTALS_ALLOWED_FOR_DOUBLE']     = conf.get('double','TOTALS_ALLOWED_FOR_DOUBLE')
        Configuration.__configuration['DOUBLE_RATIO']                  = conf.get('double','DOUBLE_RATIO')
        Configuration.__configuration['SPLIT_BY_VALUE']                = conf.getboolean('split','SPLIT_BY_VALUE')
        Configuration.__configuration['RESPLIT_UP_TO']                 = conf.get('split','RESPLIT_UP_TO')
        Configuration.__configuration['RESPLIT_ACES']                  = conf.getboolean('split','RESPLIT_ACES')
        Configuration.__configuration['HIT_SPLIT_ACES']                = conf.getboolean('split','HIT_SPLIT_ACES')
        Configuration.__configuration['SPLIT_RATIO']                   = conf.get('split','SPLIT_RATIO')
        Configuration.__configuration['LATE_SURRENDER']                = conf.getboolean('surrender','LATE_SURRENDER')
        Configuration.__configuration['LATE_SURRENDER_RATIO']          = conf.get('surrender','LATE_SURRENDER_RATIO')
        Configuration.__configuration['EARLY_SURRENDER']               = conf.getboolean('surrender','EARLY_SURRENDER')
        Configuration.__configuration['OFFER_INSURANCE']               = conf.getboolean('insurance','OFFER_INSURANCE')
        Configuration.__configuration['INSURANCE_RATIO']               = conf.get('insurance','INSURANCE_RATIO')
        Configuration.__configuration['MINIMUM_BET']                   = conf.getint('game','MINIMUM_BET')
        Configuration.__configuration['MAXIMUM_BET']                   = conf.getint('game','MAXIMUM_BET')
        Configuration.__configuration['WINNINGS_REMAIN_IN_POT']        = conf.getboolean('preferences','WINNINGS_REMAIN_IN_POT')

    @staticmethod
    def get(key):
        if key in Configuration.__configuration:
            return Configuration.__configuration[key]
        else:
            raise InvalidOptionError('Unknown configuration option:', key)

    @staticmethod
    def writeConfigFile(filename):
        """Outputs configuration to file"""
        def func(key):
            return "%s: %s\n" % (key, Configuration.__configuration[key])
        f = open(filename, 'w')
        f.write('[general]\n')
        f.write(func('BLACKJACK_VALUE'))
        f.write(func('NUM_DECKS'))
        f.write(func('PUSH_ON_BLACKJACK'))
        f.write(func('CUT_INDEX'))
        f.write(func('NUM_CARDS_BURN_ON_SHUFFLE'))
        f.write('\n')
        f.write('[payout_ratio]\n')
        f.write(func('PAYOUT_RATIO'))
        f.write(func('BLACKJACK_PAYOUT_RATIO'))
        f.write(func('INSURANCE_PAYOUT_RATIO'))
        f.write('\n')
        f.write('[dealer]\n')
        f.write(func('DEALER_HITS_ON_SOFT_17'))
        f.write(func('DEALER_CHECKS_FOR_BLACKJACK'))
        f.write('\n')
        f.write('[double]\n')
        f.write(func('DOUBLE_AFTER_SPLIT_ALLOWED'))
        f.write(func('TOTALS_ALLOWED_FOR_DOUBLE'))
        f.write(func('DOUBLE_RATIO'))
        f.write('\n')
        f.write('[split]\n')
        f.write(func('SPLIT_BY_VALUE'))
        f.write(func('RESPLIT_UP_TO'))
        f.write(func('RESPLIT_ACES'))
        f.write(func('HIT_SPLIT_ACES'))
        f.write(func('SPLIT_RATIO'))
        f.write('\n')
        f.write('[surrender]\n')
        f.write(func('LATE_SURRENDER'))
        f.write(func('LATE_SURRENDER_RATIO'))
        f.write(func('EARLY_SURRENDER'))
        f.write('\n')
        f.write('[insurance]\n')
        f.write(func('OFFER_INSURANCE'))
        f.write(func('INSURANCE_RATIO'))
        f.write('\n')
        f.write('[game]\n')
        f.write(func('MINIMUM_BET'))
        f.write(func('MAXIMUM_BET'))
        f.write('\n')
        f.write('[preferences]\n')
        f.write(func('WINNINGS_REMAIN_IN_POT'))

    @staticmethod
    def parseConfigFile(filename):
        """Parses configuration data from file"""
        conf = ConfigParser(defaults=Configuration.__configuration)
        num_read = conf.read(filename)
        if len(num_read) == 1:
            return conf
        else:
            return None

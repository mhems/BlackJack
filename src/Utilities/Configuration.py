####################
#
# Configuration.py
#
####################

from configparser import ConfigParser
import re

from src.Basic.Card import Card
from src.Utilities.Utilities import Utilities

# Make silent parsing errors notify user

class Configuration:
    """Provides handling and access of configuration files"""
    
    BLACKJACK_VALUE = 21
    RANGE_ALL = 42
    
    configuration = {
        # > 0
        'NUM_DECKS'                      : 6,
        # True | False
        'PUSH_ON_BLACKJACK'              : True,
        # > 0 => index from shoe front
        # < 0 => index from shoe rear
        'CUT_INDEX'                      : -26,
        # > 0 and < number cards in shoe
        'NUM_CARDS_BURN_ON_SHUFFLE'      : 1,

        # ratios must be floats or fractions
        'PAYOUT_RATIO'                   : '1/1',
        'BLACKJACK_PAYOUT_RATIO'         : '3/2',
        'INSURANCE_PAYOUT_RATIO'         : '2/1',

        # True | False
        'DOUBLE_AFTER_SPLIT_ALLOWED'     : True,
        # must be * or comma separated list of card ranks
        'CARDS_ALLOWED_FOR_DOUBLE'       : '*',

        # True | False
        'SPLIT_BY_VALUE'                 : True,
        # > 0
        'RESPLIT_UP_TO'                  : 4,
        # True | False
        'RESPLIT_ACES'                   : True,
        # True | False
        'HIT_SPLIT_ACES'                 : True,

        # True | False
        'DEALER_HITS_ON_SOFT_17'         : True,
        # True | False
        'DEALER_CHECKS_FOR_BLACKJACK'    : True,

        # True | False
        'LATE_SURRENDER'                 : False,
        # must be * or comma separated list of card ranks
        #'ALLOWED_LATE_SURRENDER_RANGE'   : '',
        # True | False
        'EARLY_SURRENDER'                : False,
        # must be * or comma separated list of card ranks
        #'ALLOWED_EARLY_SURRENDER_RANGE'  : ''
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
        num_decks = Configuration.configuration['NUM_DECKS']
        if num_decks < 1:
            Utilities.error('NUM_DECKS: (%d) Expected number to be at least 1' % num_decks)
        num_cards = Configuration.configuration['NUM_DECKS'] * Card.NUM_CARDS_PER_DECK
        cut_index = Configuration.configuration['CUT_INDEX']
        if abs(cut_index) > num_cards:
            Utilities.error('CUT_INDEX: (%d) Cut index cannot be greater than number of cards in shoe (%d)' % (cut_index, num_cards))
            
        if cut_index < 0:
            Configuration.configuration['CUT_INDEX'] = num_cards - abs(cut_index)
        num_burn = Configuration.configuration['NUM_CARDS_BURN_ON_SHUFFLE']
        if num_burn < 0:
            Utilities.error('NUM_CARDS_BURN_ON_SHUFFLE: (%d) Number of cards to burn after shuffle must be positive' % num_burn) 
        if num_burn > num_cards:
            Utilities.error('NUM_CARDS_BURN_ON_SHUFFLE: (%d) Number of cards to burn after shuffle must be at most the number of cards in the deck (%d)' % (num_burn, num_cards))

        Configuration.__checkRatio('PAYOUT_RATIO')
        Configuration.__checkRatio('BLACKJACK_PAYOUT_RATIO')
        Configuration.__checkRatio('INSURANCE_PAYOUT_RATIO')

        resplit_num = Configuration.configuration['RESPLIT_UP_TO']
        if resplit_num < 1:
            Utilities.error('RESPLIT_UP_TO: (%d) Number of times to resplit must be positive' % resplit_num)
        Configuration.__checkCardRange('CARDS_ALLOWED_FOR_DOUBLE')
        if Configuration.configuration['LATE_SURRENDER']:
            Configuration.__checkCardRange('ALLOWED_LATE_SURRENDER_RANGE')
        if Configuration.configuration['EARLY_SURRENDER']:
            Configuration.__checkCardRange('ALLOWED_EARLY_SURRENDER_RANGE')
        if Utilities.numErrors > 0:
            Utilities.fatalError('Fatal semantic error in configuration options, exiting now')

    @staticmethod
    def __checkRatio(flagname):
        """Semantic check of options with ratio values"""
        value = Configuration.configuration[flagname]
        if isinstance(value, float):
            Configuration.configuration[flagname] = float(value)
        else:
            match = re.match('([1-9][0-9]*)/([1-9][0-9]*)', value)
            if isinstance(value, str) and match:
                Configuration.configuration[flagname] = float(int(match.group(1))/int(match.group(2)))
            else:
                Utilities.error('%s: (%s) Ratio must be either a decimal or fraction' % (flagname, value))

    @staticmethod
    def __checkCardRange(flagname):
        """Semantic check of options with range values"""
        value = Configuration.configuration[flagname]
        if value == '*':
            Configuration.configuration[flagname] = Configuration.RANGE_ALL
        else:
            ls = list(set(re.findall('10|J|Q|K|A|[2-9]', value, re.I)))
            for idx, elem in enumerate(ls):
                if re.match('10|[2-9]', elem):
                    ls[idx] = int(elem)
            Configuration.configuration[flagname] = ls
            
    @staticmethod
    def __assign(conf):
        """Assigns values from configuration file into dictionary"""
        Configuration.configuration['NUM_DECKS']                     = conf.getint('general','NUM_DECKS')
        Configuration.configuration['PUSH_ON_BLACKJACK']             = conf.getboolean('general','PUSH_ON_BLACKJACK')
        Configuration.configuration['CUT_INDEX']                     = conf.getint('general','CUT_INDEX')
        Configuration.configuration['NUM_CARDS_BURN_ON_SHUFFLE']     = conf.getint('general','NUM_CARDS_BURN_ON_SHUFFLE')
        Configuration.configuration['PAYOUT_RATIO']                  = conf.get('payout_ratio','PAYOUT_RATIO')
        Configuration.configuration['BLACKJACK_PAYOUT_RATIO']        = conf.get('payout_ratio','BLACKJACK_PAYOUT_RATIO')
        Configuration.configuration['INSURANCE_PAYOUT_RATIO']        = conf.get('payout_ratio','INSURANCE_PAYOUT_RATIO')
        Configuration.configuration['DOUBLE_AFTER_SPLIT_ALLOWED']    = conf.getboolean('double','DOUBLE_AFTER_SPLIT_ALLOWED')
        Configuration.configuration['CARDS_ALLOWED_FOR_DOUBLE']      = conf.get('double','CARDS_ALLOWED_FOR_DOUBLE')
        Configuration.configuration['SPLIT_BY_VALUE']                = conf.getboolean('split','SPLIT_BY_VALUE')
        Configuration.configuration['RESPLIT_UP_TO']                 = conf.getint('split','RESPLIT_UP_TO')
        Configuration.configuration['RESPLIT_ACES']                  = conf.getboolean('split','RESPLIT_ACES')
        Configuration.configuration['HIT_SPLIT_ACES']                = conf.getboolean('split','HIT_SPLIT_ACES')
        Configuration.configuration['DEALER_HITS_ON_SOFT_17']        = conf.getboolean('dealer','DEALER_HITS_ON_SOFT_17')
        Configuration.configuration['DEALER_CHECKS_FOR_BLACKJACK']   = conf.getboolean('dealer','DEALER_CHECKS_FOR_BLACKJACK')
        Configuration.configuration['LATE_SURRENDER']                = conf.getboolean('surrender','LATE_SURRENDER')
        Configuration.configuration['ALLOWED_LATE_SURRENDER_RANGE']  = conf.get('surrender','ALLOWED_LATE_SURRENDER_RANGE')
        Configuration.configuration['EARLY_SURRENDER']               = conf.getboolean('surrender','EARLY_SURRENDER')
        Configuration.configuration['ALLOWED_EARLY_SURRENDER_RANGE'] = conf.get('surrender','ALLOWED_EARLY_SURRENDER_RANGE')

    @staticmethod
    def writeConfigFile(filename, dictionary):
        """Outputs dictionary to file"""
        func = lambda arg: "%s: Configuration.configuration['%s']\n"
        f = open(filename, 'w')
        f.write('[general]\n')
        f.write(func('NUM_DECKS'))
        f.write(func('PUSH_ON_BLACKJACK'))
        f.write(func('NUM_CARDS_BURN_ON_SHUFFLE'))
        f.write('\n')
        f.write('[payout_ratio]\n')
        f.write(func('PAYOUT_RATIO'))
        f.write(func('BLACKJACK_PAYOUT_RATIO'))
        f.write(func('INSURANCE_PAYOUT_RATIO'))
        f.write('\n')
        f.write('[double]\n')
        f.write(func('DOUBLE_AFTER_SPLIT_ALLOWED'))
        f.write(func('CARDS_ALLOWED_FOR_DOUBLE'))
        f.write('\n')
        f.write('[split]\n')
        f.write(func('SPLIT_BY_VALUE'))
        f.write(func('RESPLIT_UP_TO'))
        f.write(func('RESPLIT_ACES'))
        f.write(func('HIT_SPLIT_ACES'))
        f.write('\n')
        f.write('[dealer]\n')
        f.write(func('DEALER_HITS_ON_SOFT_17'))
        f.write(func('DEALER_CHECKS_FOR_BLACKJACK'))
        f.write('\n')
        f.write('[surrender]\n')
        f.write(func('LATE_SURRENDER'))
        f.write(func('ALLOWED_LATE_SURRENDER_RANGE'))
        f.write(func('EARLY_SURRENDER'))
        f.write(func('ALLOWED_EARLY_SURRENDER_RANGE'))
        f.write('\n')
        
    @staticmethod
    def parseConfigFile(filename):
        """Parses configuration data from file"""
        conf = ConfigParser(defaults=Configuration.configuration)
        num_read = conf.read(filename)
        if len(num_read) == 1:
            return conf
        else:
            return None

if __name__ == '__main__':
    Configuration.loadConfiguration()
    print(Configuration.configuration)

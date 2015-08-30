####################
#
# Configuration.py
#
####################

from configparser import ConfigParser
import re

from src.Basic.Card          import Card
from src.Utilities.Utilities import Enum
import src.Utilities.Utilities as util

class SemanticConfigError(RuntimeError):
    """Represents error for configuration value with improper semantic value"""

    def __init__(self, option, msg):
        self.option = option
        self.msg    = msg

    def __str__(self):
        return 'Expected option %s %s, received %s' % (self.option,
                                                       self.msg,
                                                       str(get(self.option)))

class InvalidOptionError(KeyError):
    """Represents error for unknown configuration option"""

    def __init__(self, option):
        self.option = option

    def __str__(self):
        return 'Invalid configuration option \'%s\'' % self.option

"""Provides handling and access of configuration files"""

UNRESTRICTED  = Enum()
configuration = {}
default_filename  = 'src/Utilities/default_config.ini'

def loadConfiguration(filename=None):
    """Loads configuration data"""
    conf = ConfigParser()
    conf.read(default_filename)
    if filename is not None:
        if len(conf.read(filename)) == 0:
            util.warn(
                'Unable to read file %s, proceeding with defaults' % filename)

    # check semantics
    blackjack = get('BLACKJACK_VALUE')
    if not isinstance(blackjack, int) or blackjack < 0:
        raise SemanticConfigError('BLACKJACK_VALUE', 'to be positive integer')
    num_decks = get('NUM_DECKS')
    if not isinstance(blackjack, int) or num_decks < 1:
        raise SemanticConfigError('NUM_DECKS', 'to be an integer greater than 0')
    num_cards = ( get('NUM_DECKS') *
                  Card.NUM_CARDS_PER_DECK )
    if abs(get('CUT_INDEX')) > num_cards:
        raise SemanticConfigError('CUT_INDEX',
                                  'to be at most the number of cards in shoe'
                                  ' (%d)' % num_cards)
    num_burn = get('NUM_CARDS_BURN_ON_SHUFFLE')
    if not isinstance(num_burn, int) or num_burn < 0:
        raise SemanticConfigError('NUM_CARDS_BURN_ON_SHUFFLE',
                                  'to be positive integer')
    if num_burn > num_cards:
        raise SemanticConfigError('NUM_CARDS_BURN_ON_SHUFFLE',
                                  'to be at most the number of cards in shoe'
                                  ' (%d)' % num_cards)
    checkRatio('payout_ratio', 'PAYOUT_RATIO')
    checkRatio('payout_ratio', 'BLACKJACK_PAYOUT_RATIO')
    checkRatio('payout_ratio', 'INSURANCE_PAYOUT_RATIO')
    checkCardRange('double',   'TOTALS_ALLOWED_FOR_DOUBLE')
    checkRatio('double',       'DOUBLE_RATIO')
    resplit_num = get('RESPLIT_UP_TO')
    if resplit_num == '*':
        configuration['split']['RESPLIT_UP_TO'] = UNRESTRICTED
    elif not re.match('0|[1-9][0-9]*', str(resplit_num)):
        raise SemanticConfigError('RESPLIT_UP_TO', 'to be non-negative integer')
    checkRatio('split',     'SPLIT_RATIO')
    checkRatio('surrender', 'LATE_SURRENDER_RATIO', False)
    checkRatio('insurance', 'INSURANCE_RATIO', False)
    min_bet = get('MINIMUM_BET')
    if not isinstance(min_bet, int) or min_bet <= 0:
        raise SemanticConfigError('MINIMUM_BET', 'to be positive integer')
    max_bet = get('MAXIMUM_BET')
    if not isinstance(max_bet, int) or max_bet <= 0 or max_bet < min_bet:
        raise SemanticConfigError('MAXIMUM_BET',
                                  'to be positive integer no less than minimum'
                                  ' bet (%d)' % min_bet)

    # commit if no semantic errors
    assign(conf)

def checkRatio(category, flagname, allowImproper=True):
    """Semantic check of options with ratio values"""
    value = get(flagname)
    ratio = None
    try:
        ratio = float(value)
        if ratio < 0:
            raise SemanticConfigError(flagname, 'to be positive')
    except ValueError:
        match = re.match('\+?([1-9][0-9]*)/([1-9][0-9]*)', value)
        if match:
            ratio = float(int(match.group(1))/int(match.group(2)))
        else:
            raise SemanticConfigError(flagname,
                                      'to be either a decimal or a fraction')
    if ratio:
        if not allowImproper and ratio > 1.0:
            raise SemanticConfigError(flagname,
                                      'to be ratio between 0 and 1 inclusive')
        else:
            configuration[category][flagname] = ratio

def checkCardRange(category, flagname):
    """Semantic check of options with range values"""
    value = get(flagname)
    if value == '*':
        configuration[category][flagname] = UNRESTRICTED
    else:
        ls = list(set(re.findall('10|J(?:ack)|Q(?:ueen)|K(?:ing)|A(?:ce)|[2-9]', value, re.I)))
        for idx, elem in enumerate(ls):
            if re.match('[1-9][0-9]*', elem):
                ls[idx] = int(elem)
        configuration[category][flagname] = ls

def assign(conf):
    """Assigns values from configuration file into dictionary"""
    def assignFromFunc(func):
        """Returns function that uses func to retrieve key"""
        def assign(category, key):
            """Assigns key in category to configuration"""
            if category not in configuration:
                configuration[category] = {}
            configuration[category][key] = func(category, key)
        return assign

    assignInt  = assignFromFunc(conf.getint)
    assignStr  = assignFromFunc(conf.get)
    assignBool = assignFromFunc(conf.getboolean)

    assignInt( 'general',      'BLACKJACK_VALUE')
    assignInt( 'general',      'NUM_DECKS')
    assignBool('general',      'PUSH_ON_BLACKJACK')
    assignInt( 'general',      'CUT_INDEX')
    assignInt( 'general',      'NUM_CARDS_BURN_ON_SHUFFLE')
    assignStr( 'payout_ratio', 'PAYOUT_RATIO')
    assignStr( 'payout_ratio', 'BLACKJACK_PAYOUT_RATIO')
    assignStr( 'payout_ratio', 'INSURANCE_PAYOUT_RATIO')
    assignBool('dealer',       'DEALER_HITS_ON_SOFT_17')
    assignBool('dealer',       'DEALER_CHECKS_FOR_BLACKJACK')
    assignBool('double',       'DOUBLE_AFTER_SPLIT_ALLOWED')
    assignStr( 'double',       'TOTALS_ALLOWED_FOR_DOUBLE')
    assignStr( 'double',       'DOUBLE_RATIO')
    assignBool('split',        'SPLIT_BY_VALUE')
    assignInt( 'split',        'RESPLIT_UP_TO')
    assignBool('split',        'RESPLIT_ACES')
    assignBool('split',        'HIT_SPLIT_ACES')
    assignStr( 'split',        'SPLIT_RATIO')
    assignBool('surrender',    'LATE_SURRENDER')
    assignStr( 'surrender',    'LATE_SURRENDER_RATIO')
    assignBool('surrender',    'EARLY_SURRENDER')
    assignBool('insurance',    'OFFER_INSURANCE')
    assignStr( 'insurance',    'INSURANCE_RATIO')
    assignInt( 'game',         'MINIMUM_BET')
    assignInt( 'game',         'MAXIMUM_BET')
    assignBool('preferences',  'WINNINGS_REMAIN_IN_POT')

def get(key):
    """Retrieve value associated with key"""
    for category in configuration.keys():
        if key in configuration[category]:
            return configuration[category][key]
    raise InvalidOptionError(key)

def representation():
    """Build string representation of all associations"""
    s = ""
    for category in configuration.keys():
        s += '[%s]' % category
        s += LINE_END
        s += LINE_END.join('%s : %s' % (key, configuration[category][key]) for key in configuration[category])
        s += LINE_END
    return s

def writeConfigFile(filename):
    """Outputs configuration to file"""
    with open(filename, 'w') as f:
        f.write(representation())

# Load eagerly on first import
loadConfiguration()

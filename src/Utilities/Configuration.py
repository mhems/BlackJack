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
        if conf.read(filename) == 0:
            util.warn('Unable to read file %s, proceeding with defaults' % filename)

    assign(conf)
    # override any options with present command line flags

    # check semantics
    blackjack = get('BLACKJACK_VALUE')
    if blackjack < 0:
        util.error(
            'BLACKJACK_VALUE: (%d) Expected number to be positive' %
            blackjack)
    num_decks = get('NUM_DECKS')
    if num_decks < 1:
        util.error(
            'NUM_DECKS: (%d) Expected number to be at least 1' %
            num_decks)
    num_cards = ( get('NUM_DECKS') *
                  Card.NUM_CARDS_PER_DECK )
    cut_index = get('CUT_INDEX')
    if abs(cut_index) > num_cards:
        util.error(
            'CUT_INDEX: (%d) Cut index cannot be greater than number of '
            'cards in shoe (%d)' % (cut_index, num_cards))
    num_burn = get('NUM_CARDS_BURN_ON_SHUFFLE')
    if num_burn < 0:
        util.error(
            'NUM_CARDS_BURN_ON_SHUFFLE: (%d) Number of cards to burn after '
            'shuffle must be positive' % num_burn)
    if num_burn > num_cards:
        util.error(
            'NUM_CARDS_BURN_ON_SHUFFLE: (%d) Number of cards to burn after '
            'shuffle must be at most the number of cards in the deck (%d)' %
            (num_burn, num_cards))
    checkRatio('payout_ratio', 'PAYOUT_RATIO')
    checkRatio('payout_ratio', 'BLACKJACK_PAYOUT_RATIO')
    checkRatio('payout_ratio', 'INSURANCE_PAYOUT_RATIO')
    checkCardRange('double', 'TOTALS_ALLOWED_FOR_DOUBLE')
    checkRatio('double', 'DOUBLE_RATIO')
    resplit_num = get('RESPLIT_UP_TO')
    if resplit_num == '*':
        configuration['split']['RESPLIT_UP_TO'] = UNRESTRICTED
    elif not re.match('0|[1-9][0-9]*', str(resplit_num)):
        util.error(
            'RESPLIT_UP_TO: (%d) Number of times to resplit must be '
            'non-negative integer' % resplit_num)
    checkRatio('split', 'SPLIT_RATIO')
    checkRatio('surrender', 'LATE_SURRENDER_RATIO', False)
    checkRatio('insurance', 'INSURANCE_RATIO', False)
    min_bet = get('MINIMUM_BET')
    if min_bet <= 0:
        util.error(
            'MINIMUM BET: (%d) Minimum amount to bet must be positive' %
            min_bet);
    max_bet = get('MAXIMUM_BET')
    if max_bet <= 0 or max_bet < min_bet:
        util.error(
            'MAXIMUM BET: (%d) Maximum amount to bet must be positive '
            'number no less than minimum bet amount (%d)' %
            (max_bet, min_bet))

    if util.numErrors > 0:
        util.fatalError(
            'Fatal semantic error in configuration options, exiting now')

def checkRatio(category, flagname, allowImproper=True):
    """Semantic check of options with ratio values"""
    value = get(flagname)
    ratio = None
    try:
        ratio = float(value)
        if ratio < 0:
            util.error('%s: (%s) Ratio must be positive' %
                            (flagname, ratio))
    except ValueError:
        match = re.match('\+?([1-9][0-9]*)/([1-9][0-9]*)', value)
        if match:
            ratio = float(int(match.group(1))/int(match.group(2)))
        else:
            util.error(
                '%s: (%s) Ratio must be either a decimal or fraction' %
                (flagname, value) )
    if ratio:
        if not allowImproper and ratio > 1.0:
            util.error(
                '%s: (%s) Ratio must be between 0 and 1, inclusive' %
                (flagname, ratio))
        else:
            configuration[category][flagname] = ratio

def checkCardRange(category, flagname):
    """Semantic check of options with range values"""
    value = get(flagname)
    if value == '*':
        configuration[category][flagname] = UNRESTRICTED
    else:
        ls = list(set(re.findall('10|J|Q|K|A|[2-9]', value, re.I)))
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
        s += '[%s]\n' % category
        s += '\n'.join('%s : %s' % (key, configuration[category][key]) for key in configuration[category])
        s += '\n'
    return s

def writeConfigFile(filename):
    """Outputs configuration to file"""
    with open(filename, 'w') as f:
        f.write(representation())

# Load eagerly on first import
loadConfiguration()

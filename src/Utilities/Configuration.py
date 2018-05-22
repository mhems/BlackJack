from collections  import OrderedDict
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

# To add new configuration option, add assignment in loadConfiguration

UNRESTRICTED  = Enum()
configuration = OrderedDict()
default_filename  = 'src/Utilities/default_config.ini'

def loadConfiguration(filename):
    """Loads configuration data"""

    def assignFromFunc(func):
        """Return function with func bound as retrieval method"""
        def assign(category, key, check=None, err=''):
            """Assign option key under category into configuration
               If check specified, perform check before assignment and
               raise SemanticConfigError with err message if check fails"""
            if conf.has_option(category, key):
                #                try:
                result = func(category, key)
                #                except ValueError as e:
                #                    # attempt to pull type from function name
                #                    typ = func.__name__
                #                    if len(typ) > 2 and 'get' == typ[:3]:
                #                        typ = typ[3:]
                #                    else:
                #                        typ = None
                #                    msg = 'type ' + typ if typ else ''
                #                    raise SemanticConfigError(key, msg)
                if result is not None:
                    if ( check is None or
                         check is not None and check(result) ):
                        configuration[category][key] = result
                    else:
                        raise SemanticConfigError(key, err)
        return assign
    posInt    = lambda x : isinstance(x, int) and x >  0
    posIntErr = 'to be positive integer'
    nonNegInt = lambda x : isinstance(x, int) and x >= 0
    nonNegIntErr = 'to be an integer greater than 0'

    conf = ConfigParser()
    if len(conf.read(filename)) == 0:
        util.warn('Unable to read file %s, proceeding with defaults' % filename)
        return

    for s in conf.sections():
        if s not in configuration:
            configuration[s] = OrderedDict()

    assignInt  = assignFromFunc(conf.getint)
    assignBool = assignFromFunc(conf.getboolean)
    assignStr  = assignFromFunc(conf.get)

    # check any semantics and assign iff valid
    assignInt('general', 'BLACKJACK_VALUE', posInt,    posIntErr)
    assignInt('general', 'NUM_DECKS',       nonNegInt, nonNegIntErr)
    assignBool('general', 'PUSH_ON_BLACKJACK')
    num_cards = get('NUM_DECKS') * Card.NUM_CARDS_PER_DECK
    assignInt('general', 'CUT_INDEX',
              lambda x : isinstance(x, int) and abs(x) <= num_cards,
              'to be at most the number of cards in shoe (%d)' % num_cards)
    assignInt('general', 'NUM_CARDS_BURN_ON_SHUFFLE', nonNegInt, nonNegIntErr)
    if get('NUM_CARDS_BURN_ON_SHUFFLE') > num_cards:
        raise SemanticConfigError('NUM_CARDS_BURN_ON_SHUFFLE',
                                  'to be at most the number of cards in shoe'
                                  ' (%d)' % num_cards)

    checkRatio(conf, 'payout_ratio', 'PAYOUT_RATIO')
    checkRatio(conf, 'payout_ratio', 'BLACKJACK_PAYOUT_RATIO')
    checkRatio(conf, 'payout_ratio', 'INSURANCE_PAYOUT_RATIO')

    assignBool('dealer', 'DEALER_HITS_ON_SOFT_17')
    assignBool('dealer', 'DEALER_CHECKS_FOR_BLACKJACK')

    assignBool('double', 'DOUBLE_AFTER_SPLIT_ALLOWED')
    checkCardRange(conf, 'double', 'TOTALS_ALLOWED_FOR_DOUBLE')
    checkRatio(conf, 'double', 'DOUBLE_RATIO')

    assignBool('split', 'SPLIT_BY_VALUE')
    resplit_num = None
    if conf.has_section('split') and conf.has_option('split', 'RESPLIT_UP_TO'):
        resplit_num = conf.getint('split', 'RESPLIT_UP_TO')
    if resplit_num is not None:
        if resplit_num == '*':
            configuration['split']['RESPLIT_UP_TO'] = UNRESTRICTED
        elif nonNegInt(resplit_num):
            configuration['split']['RESPLIT_UP_TO'] = resplit_num
        else:
            raise SemanticConfigError('RESPLIT_UP_TO', nonNegIntErr)
    assignBool('split', 'RESPLIT_ACES')
    assignBool('split', 'HIT_SPLIT_ACES')
    checkRatio(conf, 'split', 'SPLIT_RATIO')

    assignBool('surrender', 'LATE_SURRENDER')
    checkRatio(conf, 'surrender', 'LATE_SURRENDER_RATIO', False)
    assignBool('surrender', 'EARLY_SURRENDER')
    checkRatio(conf, 'surrender', 'EARLY_SURRENDER_RATIO', False)

    assignBool('insurance', 'OFFER_INSURANCE')
    checkRatio(conf, 'insurance', 'INSURANCE_RATIO', False)

    assignInt('game', 'MINIMUM_BET', posInt, posIntErr)
    min_bet = get('MINIMUM_BET')
    assignInt('game', 'MAXIMUM_BET',
              lambda x : posInt(x) and x >= min_bet,
              'to be positive integer no less than minimum bet (%d)' % min_bet)

    assignBool('preferences', 'WINNINGS_REMAIN_IN_POT')

def loadDefaultConfiguration():
    """Loads default configuration"""
    loadConfiguration(default_filename)

def checkRatio(conf, category, flagname, allowImproper=True):
    """Semantic check of options with ratio values"""
    if not conf.has_option(category, flagname):
        return None
    value = conf.get(category, flagname)
    ratio = None
    if value is None:
        return None
    try:
        ratio = float(value)
        if ratio < 0:
            raise SemanticConfigError(flagname, 'to be positive')
    except ValueError:
        match = re.match('^\+?([1-9][0-9]*)/([1-9][0-9]*)$', value)
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

def checkCardRange(conf, category, flagname):
    """Semantic check of options with range values"""
    if not conf.has_option(category, flagname):
        return None
    value = conf.get(category, flagname)
    if value is None:
        return None
    elif value == '*':
        configuration[category][flagname] = UNRESTRICTED
    else:
        # refactor to allow only ranks, raise error if anything else found
        ls = list(set(re.findall(Card.RANK_REGEX, value, re.I)))
        for idx, elem in enumerate(ls):
            if re.match('[0-9]+', elem):
                ls[idx] = int(elem)
        configuration[category][flagname] = ls

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
        s += util.LINE_END
        s += util.LINE_END.join( ('%s : %s' % (key, configuration[category][key]))
                                 for key in configuration[category] )
        s += util.LINE_END
    return s

def writeConfigFile(filename):
    """Outputs configuration to file"""
    with open(filename, 'w') as f:
        f.write(representation())

# Load eagerly on first import
loadDefaultConfiguration()

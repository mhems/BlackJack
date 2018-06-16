"""
Provides handling and access of configuration files
"""

from configparser import ConfigParser
import re

class SemanticConfigError(ValueError):
    """Represents error for configuration value with improper semantic value"""

    def __init__(self, option, msg, value):
        super().__init__()
        self.option = option
        self.msg = msg
        self.value = value

    def __str__(self):
        return 'Expected option %s %s, received %s' % (self.option,
                                                       self.msg,
                                                       self.value)

class UnknownOptionError(KeyError):
    """Represents error for unknown configuration option"""

    def __init__(self, option):
        super().__init__()
        self.option = option

    def __str__(self):
        return "Unknown configuration option '%s'" % self.option

def verifyBool(_, value):
    """Parses and verifies a boolean value"""
    if value.lower() in ['true', 'false']:
        return value.lower() == 'true', None
    return None, "to be 'true' or 'false'"

def verifyCutIndex(conf, value):
    """Parses and verifies a cut index"""
    num_cards = conf['NUM_DECKS'] * conf['NUM_CARDS_PER_DECK']
    fail = False
    try:
        parsed = int(value)
    except ValueError:
        fail = True
    if not fail:
        fail = abs(parsed) > num_cards
    if fail:
        return None, 'to be within the number of cards in the shoe (%d)' % num_cards
    return parsed, None

def verifyInfiniteInt(conf, value):
    """Parses and verifies an unrestricted value or integer"""
    if value == '*':
        return Config.UNRESTRICTED, None
    parsed, err = verifyNonNegativeInt(conf, value)
    if err is None:
        return parsed, None
    return None, "to be either '*' or a non-negative integer"

def verifyMaxBet(conf, value):
    """Parses and verifies a maximum bet"""
    min_bet = conf['MINIMUM_BET']
    parsed, err = verifyPositiveInt(conf, value)
    if err is None:
        fail = parsed < min_bet
    if err is not None or fail:
        return None, 'to be an integer no less than the minimum bet (%d)' % min_bet
    return parsed, None

def verifyNonNegativeInt(_, value):
    """Parses and verifies a non-negative integer"""
    fail = False
    try:
        parsed = int(value)
    except ValueError:
        fail = True
    if not fail:
        fail = parsed < 0
    if fail:
        return None, 'to be a non-negative integer'
    return parsed, None

def verifyNumCardsBurn(conf, value):
    """Parses and verifies the number of cards to burn"""
    num_cards = conf['NUM_DECKS'] * conf['NUM_CARDS_PER_DECK']
    msg = 'to be a non-negative integer no more than the number of cards in the shoe (%d)' % num_cards
    parsed, err = verifyNonNegativeInt(conf, value)
    if err is None:
        fail = parsed > num_cards
    if err is not None or fail:
        return None, msg
    return parsed, None

def verifyPositiveInt(_, value):
    """Parses and verifies a positive integer"""
    fail = False
    try:
        parsed = int(value)
    except ValueError:
        fail = True
    if not fail:
        fail = parsed <= 0
    if fail:
        return None, 'to be positive integer'
    return parsed, None

def verifyRange(conf, value):
    """Parses and verifies a range of hand totals"""
    low = 4
    high = conf['BLACKJACK_VALUE']
    msg = 'to be a comma-separated list of integers between %d and %d' % (low, high)
    if value == '*':
        return Config.UNRESTRICTED, None
    totals = []
    fail = True
    try:
        value = value.strip('[]')
        for total in value.split(','):
            temp = int(total)
            if temp < low or temp > high:
                break
            totals.append(temp)
        else:
            fail = False
    except ValueError:
        fail = True
    if fail:
        return None, msg
    return totals, None

def verifyRatio(_, value):
    """Parses and verifies a ratio expressed as a decimal or fraction"""
    fail = False
    try:
        parsed = float(value)
    except ValueError:
        fail = True
    if not fail and parsed > 0:
        return parsed, None
    match = re.match('^\\+?([1-9][0-9]*)/([1-9][0-9]*)$', value)
    if match:
        return float(int(match.group(1))/int(match.group(2))), None
    return None, 'to be a positive decimal or fraction'


class Config:
    """Class to manage application configuration"""

    UNRESTRICTED = -1

    default_filename  = 'cfg/default_config.ini'

    _deps = {
        'CUT_INDEX': ['NUM_DECKS', 'NUM_CARDS_PER_DECK'],
        'MAXIMUM_BET': ['MINIMUM_BET'],
        'NUM_CARDS_BURN_ON_SHUFFLE': ['NUM_DECKS', 'NUM_CARDS_PER_DECK'],
        'TOTALS_ALLOWED_FOR_DOUBLE': ['BLACKJACK_VALUE'],
    }

    _key_map = {
        'BLACKJACK_VALUE': verifyPositiveInt,
        'NUM_DECKS': verifyNonNegativeInt,
        'NUM_CARDS_PER_DECK': verifyNonNegativeInt,
        'PUSH_ON_BLACKJACK': verifyBool,
        'CUT_INDEX': verifyCutIndex,
        'NUM_CARDS_BURN_ON_SHUFFLE': verifyNumCardsBurn,
        'MINIMUM_BET': verifyPositiveInt,
        'MAXIMUM_BET': verifyMaxBet,
        'NUM_SEATS': verifyPositiveInt,
        'PAYOUT_RATIO': verifyRatio,
        'BLACKJACK_PAYOUT_RATIO': verifyRatio,
        'INSURANCE_PAYOUT_RATIO': verifyRatio,
        'DEALER_HITS_ON_SOFT_17': verifyBool,
        'DEALER_CHECKS_FOR_BLACKJACK': verifyBool,
        'DOUBLE_AFTER_SPLIT_ALLOWED': verifyBool,
        'TOTALS_ALLOWED_FOR_DOUBLE': verifyRange,
        'DOUBLE_RATIO': verifyRatio,
        'SPLIT_BY_VALUE': verifyBool,
        'RESPLIT_UP_TO': verifyInfiniteInt,
        'RESPLIT_ACES': verifyBool,
        'HIT_SPLIT_ACES': verifyBool,
        'SPLIT_RATIO': verifyRatio,
        'LATE_SURRENDER': verifyBool,
        'LATE_SURRENDER_RATIO': verifyRatio,
        'EARLY_SURRENDER': verifyBool,
        'EARLY_SURRENDER_RATIO': verifyRatio,
        'OFFER_INSURANCE': verifyBool,
        'INSURANCE_RATIO': verifyRatio,
    }

    def __init__(self):
        """Create a new Config object"""
        self.parser = ConfigParser()
        self.items = {}

    @staticmethod
    def load(filename=None):
        """Load a Config object from a config file"""
        if filename is not None:
            conf = Config.load()
            conf.mergeFile(filename)
            return conf
        conf = Config()
        if filename is None:
            filename = Config.default_filename
        conf.parser.read(filename)
        for section in conf.parser.sections():
            for key, value in conf.parser.items(section):
                conf.__setitem__(key, value)
        return conf

    def merge(self, conf):
        """Merge an existing Config object into this instance"""
        for key, value in conf:
            self.items[key.upper()] = value

    def mergeFile(self, filename):
        """Merge config options from file into this instance"""
        conf = ConfigParser()
        conf.read(filename)
        for section in conf.sections():
            for key, value in conf.items(section):
                self.__setitem__(key, value)

    def keys(self):
        """Returns the keys of this instance"""
        return self.items.keys()

    def writeToFile(self, filename):
        """Writes this instance to file"""
        for section in self.parser.sections():
            for key in self.parser.options(section):
                self.parser.set(section, key, self.__getitem__(key))
        with open(filename, 'w') as fp:
            self.parser.write(fp)

    def __eq__(self, other):
        """Returns True iff this instance is equal to other"""
        return self.items == other

    def __ne__(self, other):
        """Returns True iff this instance is not equal to other"""
        return not self == other

    def __contains__(self, key):
        """Returns True iff this instance contains key"""
        return key.upper() in self.items

    def __len__(self):
        """Returns the number of config options in this instance"""
        return len(self.items)

    def __iter__(self):
        """Returns an iterable over this instance's options"""
        return iter(self.items.items())

    def __getitem__(self, key):
        """Gets the value associated with this instance's key"""
        if key.upper() in self.items:
            return self.items[key.upper()]
        raise UnknownOptionError(key)

    def __setitem__(self, key, value):
        """Sets the value associated with this instance's key"""
        parsed, err = Config._key_map[key.upper()](self, value)
        if err is None:
            self.items[key.upper()] = parsed
        else:
            raise SemanticConfigError(key, err, value)

cfg = Config.load()

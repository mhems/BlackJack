####################
#
# Configuration.py
#
####################

from configparser import ConfigParser

class Configuration:

    configuration = {
        'NUM_DECKS'                      : 6,
        'PUSH_ON_BLACKJACK'              : True,
        'CUT_INDEX'                      : 26,
        'NUM_CARDS_BURN_ON_SHUFFLE'      : 1,

        'PAYOUT_RATIO'                   : '2/1',
        'BLACKJACK_PAYOUT_RATIO'         : '3/2',
        'INSURANCE_PAYOUT_RATIO'         : '2/1',

        'DOUBLE_AFTER_SPLIT_ALLOWED'     : True,
        'CARDS_ALLOWED_FOR_DOUBLE'       : '*',

        'RESPLIT_UP_TO'                  : 4,
        'RESPLIT_ACES'                   : True,
        'HIT_SPLIT_ACES'                 : True,

        'DEALER_HITS_ON_SOFT_17'         : True,
        'DEALER_CHECKS_FOR_BLACKJACK'    : True,

        'LATE_SURRENDER'                 : False,
        'ALLOWED_LATE_SURRENDER_RANGE'   : '',
        'EARLY_SURRENDER'                : False,
        'ALLOWED_EARLY_SURRENDER_RANGE'  : ''
    }
    
    @staticmethod
    def loadConfiguration():
        res = None #parse(command_line_filename)
        if res:
            Configuration.__assign(res)
        else:
            res = parse('config.ini')
            if res:
                Configuration.__assign(res)
        # override any options with present command line flags
        # check semantics
        num_cards = Configuration.configuration['NUM_DECKS'] * Shoe.NUM_CARDS_PER_DECK
        Configuration.__checkInt('NUM_DECKS',1)
        Configuration.__checkInt('CUT_INDEX',0,num_cards)
        Configuration.__checkInt('NUM_CARDS_BURN_ON_SHUFFLE',0,num_cards)
        Configuration.__checkInt('RESPLIT_UP_TO',0)
        Configuration.__checkRatio('PAYOUT_RATIO')
        Configuration.__checkRatio('BLACKJACK_PAYOUT_RATIO')
        Configuration.__checkRatio('INSURANCE_PAYOUT_RATIO')
        Configuration.__checkCardRange('CARDS_ALLOWED_FOR_DOUBLE')
        if Configuration.configuration['LATE_SURRENDER']:
            Configuration.__checkCardRange('ALLOWED_LATE_SURRENDER_RANGE')
        if Configuration.configuration['EARLY_SURRENDER']:
            Configuration.__checkCardRange('ALLOWED_EARLY_SURRENDER_RANGE')
        if Utilities.numErrors() > 0:
            Utilities.fatalError('Fatal semantic error in Configuration.configuration options, exiting now')

    @staticmethod            
    def __checkInt(flagname,low,high=None):
        pass

    @staticmethod
    def __checkRatio(flagname):
        pass

    @staticmethod
    def __checkCardRange(flagname):
        pass
                                                                     
    @staticmethod
    def __assign(conf):
        Configuration.configuration['NUM_DECKS']                     = conf.getint('general','NUM_DECKS')
        Configuration.configuration['PUSH_ON_BLACKJACK']             = conf.getboolean('general','PUSH_ON_BLACKJACK')
        Configuration.configuration['CUT_INDEX']                     = conf.getint('general','CUT_INDEX')
        Configuration.configuration['NUM_CARDS_BURN_ON_SHUFFLE']     = conf.getint('general','NUM_CARDS_BURN_ON_SHUFFLE')
        Configuration.configuration['PAYOUT_RATIO']                  = conf.get('payout_ratio','PAYOUT_RATIO')
        Configuration.configuration['BLACKJACK_PAYOUT_RATIO']        = conf.get('payout_ratio','BLACKJACK_PAYOUT_RATIO')
        Configuration.configuration['INSURANCE_PAYOUT_RATIO']        = conf.get('payout_ratio','INSURANCE_PAYOUT_RATIO')
        Configuration.configuration['DOUBLE_AFTER_SPLIT_ALLOWED']    = conf.getboolean('double','DOUBLE_AFTER_SPLIT_ALLOWED')
        Configuration.configuration['CARDS_ALLOWED_FOR_DOUBLE']      = conf.get('double','CARDS_ALLOWED_FOR_DOUBLE')
        Configuration.configuration['RESPLIT_UP_TO']                 = conf.getint('split','RESPLIT_UP_TO')
        Configuration.configuration['RESPLIT_ACES']                  = conf.getboolean('split','RESPLIT_ACES')
        Configuration.configuration['HIT_SPLIT_ACES']                = conf.getboolean('split','HIT_SPLIT_ACES')
        Configuration.configuration['DEALER_HITS_ON_SOFT_17']        = conf.getboolean('dealer','DEALER_HITS_ON_SOFT_17')
        Configuration.configuration['DEALER_CHECKS_FOR_BLACKJACK']   = conf.getboolean('dealer','DEALER_CHECKS_FOR_BLACKJACK')
        Configuration.configuration['LATE_SURRENDER']                = conf.getboolean('surrender','LATE_SURRENDER')
        Configuration.configuration['ALLOWED_LATE_SURRENDER_RANGE']  = conf.get('surrender','ALLOWED_LATE_SURRENDER_RANGE')
        Configuration.configuration['EARLY_SURRENDER']               = conf.getboolean('surrender','EARLY_SURRENDER')
        Configuration.configuration['ALLOWED_EARLY_SURRENDER_RANGE'] = conf.get('surrender','ALLOWED_EARLY_SURRENDER_RANGE')

def parse(filename):
    conf = ConfigParser(defaults=Configuration.configuration)
    num_read = conf.read(filename)
    if len(num_read) == 1:
        return conf
    else:
        return None

Configuration.load()
print(Configuration.configuration)

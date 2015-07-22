####################
#
# Table.py
#
####################

from src.Utilities.Configuration import Configuration
from src.Utilities.Utilities     import Utilities
from src.Basic.Card import Card
from src.Basic.BlackjackHand import BlackjackHand
from src.Basic.Shoe import Shoe
from src.Basic.Shoe import faro_shuffle
from src.Basic.Shoe import fisher_yates_shuffle
from src.Game.TableSlot import TableSlot
from src.Game.HouseBank import HouseBank
from src.Game.Dealer    import Dealer
from src.Logic.Command       import Command
from src.Logic.HitCommand    import HitCommand
from src.Logic.StandCommand  import StandCommand
from src.Logic.DoubleCommand import DoubleCommand
from src.Logic.SplitCommand  import SplitCommand
from src.Logic.SurrenderCommand  import SurrenderCommand

class Table:
    """Representation of Blackjack Table"""

    def __init__(self, num_slots = 6):
        """Initializes table members"""
        self.__dealer_slot = TableSlot()
        self.__bank        = HouseBank()
        self.__num_slots   = num_slots
        # Index 0 is dealer's leftmost slot
        self.__slots       = [TableSlot() for _ in range(self.__num_slots)]
        self.__shoe        = Shoe(Configuration.get('NUM_DECKS'),
                                  fisher_yates_shuffle,
                                  Configuration.get('CUT_INDEX'))
        self.__shoe.shuffle()
        self.__dealer_slot.seatPlayer(Dealer())
        hitCmd   = HitCommand(self.__shoe)
        standCmd = StandCommand()
        self.__commands    = {
            Command.HIT_ENUM       : hitCmd,
            Command.STAND_ENUM     : standCmd,
            Command.DOUBLE_ENUM    : DoubleCommand(hitCmd, standCmd),
            Command.SPLIT_ENUM     : SplitCommand(hitCmd,  standCmd),
            Command.SURRENDER_ENUM : SurrenderCommand()
        }
        
    @property
    def dealer(self):
        """Returns table dealer"""
        return self.__dealer_slot.player
        
    @property
    def slots(self):
        """Returns generator for all slots at table"""
        return (self.__slots[i] for i in range(self.__num_slots))

    @property
    def occupied_slots(self):
        """Returns generator for all slots with players at table"""
        return (slot for slot in self.__slots if slot.isOccupied)

    @property
    def active_slots(self):
        """Returns generator for all slots with active players at table"""
        return (slot for slot in self.__slots if slot.isActive)

    @property
    def dealerHasBlackjack(self):
        """Returns True iff dealer has natural blackjack"""
        return self.__dealer_slot.hasBlackjack

    @property
    def num_vacancies(self):
        """Number of vacant seats at table"""
        return len(s for s in self.__slots if s is None)

    @property
    def num_players(self):
        """Number of players seated at table"""
        return self.num_slots - self.num_vacancies

    @property
    def num_active_players(self):
        """Number of players with placed bets"""
        return len(s for s in self.__slots if s.isActive)
    
    def register_player(self, player, pos=-1):
        """Register player to table, provided there is room"""
        if pos < 0:
            # Look from dealer's left to right for opening
            for slot in self.slots:
                if not slot.isOccupied:
                    slot.seatPlayer(player)
                    return True
            return False
        elif pos > self.__num_slots:
            return False
        else:
            return self.__slots[pos].isOccupied
        
    def play(self):
        """Plays one round of blackjack"""
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
              '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        dealerHasBlackjack = False
        for slot in self.__slots:
            slot.beginRound()
        self.__dealer_slot.beginRound()
        for slot in self.occupied_slots:
            slot.promptBet()
        upcard = self.__dealCards()
        print('Dealer shows', upcard.rank)
        if Configuration.get('EARLY_SURRENDER'):
            self.__offer_early_surrender()
        if ( upcard.value == ( Configuration.get('BLACKJACK_VALUE') -
                               Card.HARD_ACE_VALUE ) and
             self.__dealer_slot.hasNaturalBlackjack ):
            dealerHasBlackjack = True
            print('Dealer has blackjack')
        if Configuration.get('OFFER_INSURANCE') and upcard.isAce:
            for slot in self.active_slots:
                slot.promptInsurance()
            dealerHasBlackjack = self.__dealer_slot.hasNaturalBlackjack
            buffer = "has" if dealerHasBlackjack else "doesn't have"
            print('Dealer %s blackjack' % buffer)
        if dealerHasBlackjack:
            for slot in self.active_slots:
                if not slot.hasNaturalBlackjack:
                    self.__bank.deposit(slot.takePot())
                if slot.insured:
                    print('You\'re insured though')
                    slot.payToPot( self.__bank.withdraw(slot.insurance *
                                   Configuration.get('INSURANCE_PAYOUT_RATIO') ) )
                slot.settled = True
        else:
            for slot in self.active_slots:
                dealerActs = False
                self.__bank.deposit(slot.takeInsurance())
                if slot.hasNaturalBlackjack:
                    print('BLACKJACK!')
                    slot.payToPot( self.__bank.withdraw(slot.pot *
                                   Configuration.get('BLACKJACK_PAYOUT_RATIO') ) )
                    slot.settled = True
                else:
                    dealerActs = True
                    Utilities.printBanner('PLAYER: %s' % slot.playerName)
                    self.__dealToSlot(slot, upcard)
                    print()
            if dealerActs:
                Utilities.printBanner('DEALER')
                self.__dealToSlot(self.__dealer_slot, upcard)
                print()
        self.__settle_bets()
        for slot in self.occupied_slots:
            slot.endRound()
        self.__dealer_slot.clearHands()
        for slot in self.occupied_slots:
            print('%s plus $%d in pot' % (slot.player, slot.pot))
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
              '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')

    def __dealToSlot(self, slot, upcard):
        """Manages turn for active slot"""
        for index, hand in enumerate(slot.hands):
            slot.index = index
            done = False
            while not done:
                print('deal:', hand.value)
                if hand.isBlackjackValued:
                    break
                if hand.isBust:
                    self.__bank.deposit(slot.takePot())
                    slot.settled = True
                    break
                actions = [key for (key, cmd) in self.__commands.items()
                           if cmd.isAvailable(slot)]
                response = slot.promptAction(upcard, actions)
                if response == Command.SURRENDER_ENUM:
                    self.__bank.deposit(
                        slot.takePot(Configuration.get('LATE_SURRENDER_RATIO')) )
                done = self.__commands[response].execute(slot)
            print('Hand ends at', hand.value)

    def __offer_early_surrender(self):
        """Offers early surrender to each active player"""
        for slot in self.active_slots:
            slot.promptEarlySurrender()
            if slot.surrendered:
                self.__bank.deposit(
                    slot.takePot(Configuration.get('EARLY_SURRENDER_RATIO')) )
            
    def __settle_bets(self):
        """Settles each active player's 
           Assumes:
              * each player's hands are not bust, natural, or surrendered
              * dealer does not have natural"""
        dealer_value = self.__dealer_slot.handValue
        for slot in self.active_slots:
            if not slot.settled:
                for index, hand in enumerate(slot.hands):
                    slot.index = index
                    value = hand.value
                    if value > dealer_value or self.__dealer_slot.handIsBust:
                        slot.payToPot( self.__bank.withdraw(
                                       slot.pot *
                                       Configuration.get('PAYOUT_RATIO') ) )
                    elif value < dealer_value:
                        self.__bank.deposit(slot.takePot())
        
    def __dealCards(self):
        """Deals hands to all active players
           Returns dealer's up card"""
        for slot in self.active_slots:
            slot.addCards(self.__shoe.dealOneCard())
        self.__dealer_slot.addCards(self.__shoe.dealOneCard())
        for slot in self.active_slots:
            slot.addCards(self.__shoe.dealOneCard())
        upcard = self.__shoe.dealOneCard()
        self.__dealer_slot.addCards(upcard)
        return upcard
        
    def unregister_player(self, player):
        """Unregister player from table"""
        for pos, slot in self.occupied_slots:
            if slot.player == player:
                self.unregister_player_from_slot(pos)
                    
    def unregister_player_from_slot(self, pos):
        """Unregister player from slot, if present"""
        if self.__slots[pos].isOccupied:
            self.__slots[pos].unseatPlayer()

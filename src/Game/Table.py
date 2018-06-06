from math import floor

import src.Utilities.Configuration as config
from src.Basic.Shoe import Shoe
from src.Basic.Shoe import fisher_yates_shuffle
from src.Game.TableSlot import TableSlot
from src.Game.Bank import Bank
from src.Game.Player import Dealer
from src.Logic.CardCount     import HiLoCount
from src.Logic.Command import (Command,
                               HitCommand,
                               StandCommand,
                               DoubleCommand,
                               SplitCommand,
                               SurrenderCommand)


class Table:
    """Representation of Blackjack Table"""

    def __init__(self, num_slots = 6):
        """Initializes table members"""
        self.dealer_slot = TableSlot()
        self.bank = Bank()
        self.num_slots = num_slots
        # Index 0 is dealer's leftmost slot
        self.slots = [TableSlot() for _ in range(self.num_slots)]
        self.shoe = Shoe(config.get('NUM_DECKS'),
                         fisher_yates_shuffle,
                         config.get('CUT_INDEX'))
        self.shoe.shuffle()
        self.shoe.registerObserver(HiLoCount())
        self.dealer_slot.seatPlayer(Dealer())
        hitCmd = HitCommand(self.shoe)
        standCmd = StandCommand()
        self.commands = {
            Command.HIT       : hitCmd,
            Command.STAND     : standCmd,
            Command.DOUBLE    : DoubleCommand(hitCmd, standCmd),
            Command.SPLIT     : SplitCommand(hitCmd, standCmd),
            Command.SURRENDER : SurrenderCommand()
        }

    @property
    def all_slots(self):
        """Returns generator for all slots at table"""
        yield from self.slots

    @property
    def occupied_slots(self):
        """Returns generator for all slots with players at table"""
        return (slot for slot in self.slots if slot.isOccupied)

    @property
    def active_slots(self):
        """Returns generator for all slots with active players at table"""
        return (slot for slot in self.slots if slot.isActive)

    @property
    def num_vacancies(self):
        """Number of vacant seats at table"""
        return len(s for s in self.slots if s is None)

    @property
    def num_players(self):
        """Number of players seated at table"""
        return self.num_slots - self.num_vacancies

    @property
    def num_active_players(self):
        """Number of players with placed bets"""
        return len(s for s in self.slots if s.isActive)

    def register_player(self, player, pos=-1):
        """Register player to table, provided there is room"""
        if pos < 0:
            # Look from dealer's left to right for opening
            for slot in self.slots:
                if not slot.isOccupied:
                    slot.seatPlayer(player)
                    return True
            return False
        if pos > self.num_slots:
            return False
        if not self.slots[pos].isOccupied:
            self.slots[pos].seatPlayer(player)
            return True
        return False

    def beginRound(self):
        print('>' * 80)
        for slot in self.occupied_slots:
            slot.beginRound()
        self.dealer_slot.beginRound()
        upcard = self.dealCards()
        print('Dealer shows', upcard.rank)
        return upcard

    def endRound(self):
        self.settle_bets()
        for slot in self.occupied_slots:
            slot.endRound()
        self.dealer_slot.endRound()
        for slot in self.occupied_slots:
            print('%s plus $%d in pot' % (slot.player, slot.pot))
        print('<' * 80)

    def play(self):
        """Plays one round of blackjack"""

        upcard = self.beginRound()
        if config.get('EARLY_SURRENDER'):
            self.offer_early_surrender()
        if self.dealer_slot.hand.isNaturalBlackjack:
            self.handle_dealer_blackjack(upcard)
        else:
            for slot in self.active_slots:
                dealerActs = False
                self.bank.deposit(slot.takeInsurance())
                if slot.hand.isNaturalBlackjack:
                    print('BLACKJACK!')
                    self.payout( slot,
                                 slot.pot * config.get('BLACKJACK_PAYOUT_RATIO') )
                    slot.settled = True
                else:
                    dealerActs = True
                    print('PLAYER: %s' % slot.player.name)
                    self.dealToSlot(slot, upcard)
                    print()
            if dealerActs:
                print('DEALER')
                self.dealToSlot(self.dealer_slot, upcard)
                print()

        self.endRound()

    def payout(self, slot, amt):
        """Pay floor of amt to slot"""
        slot.payToPot(self.bank.withdraw(floor(amt)))

    def dealToSlot(self, slot, upcard):
        """Manages turn for active slot"""
        for hand in slot.hands:
            done = False
            while not done:
                if hand.isBlackjackValued:
                    break
                if hand.isBust:
                    self.bank.deposit(slot.takePot())
                    slot.settled = True
                    break
                actions = [key for (key, cmd) in self.commands.items()
                           if cmd.isAvailable(slot)]
                response = slot.promptAction(upcard, actions)
                if response == 'Su':
                    slot.surrendered = True
                    self.bank.deposit(
                        slot.takePot(config.get('LATE_SURRENDER_RATIO')) )
                done = self.commands[response].execute(slot)
            print('Hand ends at', hand.value)

    def offer_early_surrender(self):
        """Offers early surrender to each active player"""
        for slot in self.active_slots:
            slot.promptEarlySurrender()
            if slot.surrendered:
                self.bank.deposit(
                    slot.takePot(config.get('EARLY_SURRENDER_RATIO')) )

    def settle_bets(self):
        """Settles each active player's bet(s)
           Assumes:
              * each player's hands are not bust, natural, or surrendered
              * dealer does not have natural blackjack"""
        dealer_value = self.dealer_slot.hand.value
        for slot in self.active_slots:
            if not slot.settled:
                for index in range(len(slot.hands)):
                    slot.index = index
                    value = slot.hand.value
                    if value > dealer_value or self.dealer_slot.hand.isBust:
                        self.payout(slot, slot.pot *
                                    config.get('PAYOUT_RATIO') )
                    elif value < dealer_value:
                        self.bank.deposit(slot.takePot())

    def dealCards(self):
        """Deals hands to all active players
           Returns dealer's up card"""
        for slot in self.active_slots:
            slot.addCards(self.shoe.dealOneCard())
        self.dealer_slot.addCards(self.shoe.dealOneCard(False))
        for slot in self.active_slots:
            slot.addCards(self.shoe.dealOneCard())
        upcard = self.shoe.dealOneCard()
        self.dealer_slot.addCards(upcard)
        return upcard

    def unregister_player(self, player):
        """Unregister player from table"""
        for pos, slot in self.occupied_slots:
            if slot.player == player:
                self.unregister_player_from_slot(pos)

    def unregister_player_from_slot(self, pos):
        """Unregister player from slot, if present"""
        if self.slots[pos].isOccupied:
            self.slots[pos].unseatPlayer()


    def handle_dealer_blackjack(self, upcard):
        """Handles the event dealer is dealt a natural blackjack"""
        if config.get('OFFER_INSURANCE') and upcard.isAce:
            for slot in self.active_slots:
                slot.promptInsurance()
        print('Dealer has blackjack')
        for slot in self.active_slots:
            if not slot.hand.isNaturalBlackjack:
                self.bank.deposit(slot.takePot())
            if slot.insured:
                print("You're insured though")
                self.payout(slot,
                            slot.insurance * config.get('INSURANCE_PAYOUT_RATIO'))
            slot.settled = True

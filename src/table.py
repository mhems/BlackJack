from math import floor

from cards import (BlackjackHand, Shoe, fisher_yates_shuffle)
from commands import (Command,
                      HitCommand,
                      StandCommand,
                      DoubleCommand,
                      SplitCommand,
                      SurrenderCommand)
from config import get
from game import (Bank, Dealer)
from policies import CardCount

class Table:
    """Representation of Blackjack Table"""

    def __init__(self, num_slots = 6):
        """Initializes table members"""
        self.dealer_slot = TableSlot()
        self.num_slots = num_slots
        # Index 0 is dealer's leftmost slot
        self.slots = [TableSlot() for _ in range(self.num_slots)]
        self.shoe = Shoe(get('NUM_DECKS'),
                         fisher_yates_shuffle,
                         get('CUT_INDEX'))
        self.shoe.shuffle()
        self.shoe.registerObserver(CardCount('HiLoCount'))
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
    def bank(self):
        """Returns the table's dealer's bank"""
        return self.dealer_slot.player.stack

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
            print(slot.player)
        print(self.dealer_slot.player)
        print('<' * 80)

    def play(self):
        """Plays one round of blackjack"""

        upcard = self.beginRound()
        if get('EARLY_SURRENDER'):
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
                                 slot.pot * get('BLACKJACK_PAYOUT_RATIO') )
                    slot.settled = True
                else:
                    dealerActs = True
                    print('PLAYER: %s' % slot.player.name)
                    self.dealSlot(slot, upcard)
                    print()
            if dealerActs:
                print('DEALER')
                self.dealSlot(self.dealer_slot, upcard)
                print()

        self.endRound()

    def payout(self, slot, amt):
        """Pay floor of amt to slot"""
        slot.payToPot(self.bank.withdraw(floor(amt)))

    def dealHand(self, i, slot, upcard):
        """Deals a hand within a slot"""
        while True:
            hand = slot.hands[i]
            if hand.isBlackjackValued:
                break
            if hand.isBust:
                self.bank.deposit(slot.takePot())
                slot.settled = True
                break
            actions = [key for (key, cmd) in self.commands.items()
                       if cmd.isAvailable(slot)]
            response = slot.promptAction(upcard, actions)
            if response == Command.SURRENDER:
                slot.surrendered = True
                self.bank.deposit(slot.takePot(get('LATE_SURRENDER_RATIO')))
            if self.commands[response].execute(slot):
                break
        print('Hand ends at', hand.value)

    def dealSlot(self, slot, upcard):
        """Manages turn for active slot"""
        i = 0
        while i < len(slot.hands):
            slot.index = i
            self.dealHand(i, slot, upcard)
            i += 1

    def offer_early_surrender(self):
        """Offers early surrender to each active player"""
        for slot in self.active_slots:
            slot.promptEarlySurrender()
            if slot.surrendered:
                self.bank.deposit(
                    slot.takePot(get('EARLY_SURRENDER_RATIO')) )

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
                                    get('PAYOUT_RATIO') )
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
        if get('OFFER_INSURANCE') and upcard.isAce:
            for slot in self.active_slots:
                slot.promptInsurance()
        print('Dealer has blackjack')
        for slot in self.active_slots:
            if not slot.hand.isNaturalBlackjack:
                self.bank.deposit(slot.takePot())
            if slot.insured:
                print("You're insured though")
                self.payout(slot,
                            slot.insurance * get('INSURANCE_PAYOUT_RATIO'))
            slot.settled = True

class TableSlot:
    """Representation of one seat at the table (player, pot, hand)"""

    def __init__(self):
        self.player = None
        self.hands = [BlackjackHand()]
        self.pots = [0]
        self.insurance = 0
        self.insured = False
        self.index = 0
        self.surrendered = False
        self.settled = False

    @property
    def hand(self):
        """Return current hand being acted upon"""
        return self.hands[self.index]

    @property
    def pot(self):
        """Return amount of money in current pot"""
        return self.pots[self.index]

    @property
    def firstAction(self):
        """Return True iff player is on first action for hand"""
        return self.hand.numCards == 2

    @property
    def numSplits(self):
        """Returns number of times player has split this round"""
        return len(self.hands) - 1

    @property
    def playerCanAffordDouble(self):
        """Return True iff player has adequate funds to double"""
        return self._canAfford('DOUBLE_RATIO')

    @property
    def playerCanAffordSplit(self):
        """Return True iff player has adequate funds to split"""
        return self._canAfford('SPLIT_RATIO')

    @property
    def playerCanAffordInsurance(self):
        """Return True iff player has adequate funds to insurance"""
        return self._canAfford('INSURANCE_RATIO')

    @property
    def isActive(self):
        """Return True iff seated player has placed money to play"""
        return self.pots[0] > 0

    @property
    def isOccupied(self):
        """Return True iff slot has seated player"""
        return self.player != None

    def seatPlayer(self, player):
        """Seats player at table slot"""
        self.player = player

    def unseatPlayer(self):
        """Removes player from table slot"""
        self.player = None

    def addCards(self, *cards):
        """Adds card to hand"""
        self.hand.addCards(*cards)

    def beginRound(self):
        """Executes any actions necessary to begin turn"""
        self.promptBet()

    def endRound(self):
        """Executes any actions necessary to end turn"""
        if self.isOccupied:
            self.player.receive_payment(sum(self.pots))
            self.player.receive_payment(self.insurance)
        self.pots = [0]
        self.insurance = 0
        self.insured = False
        self.index = 0
        self.settled = False
        self.surrendered = False
        self.clearHands()

    def clearHands(self):
        """Resets any hands in slot"""
        self.hands = [self.hands[0]]
        self.hands[0].reset()

    def promptAction(self, upcard, availableCommands, **kwargs):
        """Prompts player to act"""
        return self.player.act(self.hand, upcard, availableCommands, **kwargs)

    def promptInsurance(self, **kwargs):
        """Prompts player for insurance"""
        if ( self.playerCanAffordInsurance and
             self.player.insure(self.hand,**kwargs) ):
            self.insured = True
            self.insurance = self.player.wager(
                self.pots[0] * get('INSURANCE_RATIO'))

    def promptBet(self, **kwargs):
        """Prompts player to bet"""
        amt = self.player.amountToBet(**kwargs)
        if amt >= self.pot:
            self.pots[self.index] += self.player.wager(amt - self.pot)
        else:
            self.player.receive_payment(self.pot - amt)

    def promptEarlySurrender(self, upcard, **kwargs):
        """Prompts player for early surrender"""
        if self.player.earlySurrender(self.hand, upcard, **kwargs):
            pass

    def takePot(self, fraction=1):
        """Takes and returns specified fraction of pot"""
        amt = floor(self.pot * fraction)
        self.pots[self.index] -= amt
        return amt

    def takeInsurance(self):
        """Takes and empties insurance"""
        amt = self.insurance
        self.insurance = 0
        return amt

    def payToPot(self, amt):
        """Places amt in pot"""
        self.pots[self.index] += amt

    def splitHand(self):
        """Splits player's hand into 2 new hands with one card each"""
        (card1, card2) = self.hand.splitCards
        self.hands[self.index] = BlackjackHand()
        self.hands[self.index].addCards(card1)
        self.hands[self.index].wasSplit = True
        self.hands.insert(self.index + 1, BlackjackHand())
        split_bet = floor( self.pots[self.index] *
                           get('SPLIT_RATIO') )
        self.player.wager(split_bet)
        self.pots.insert(self.index + 1, split_bet)
        self.hands[self.index + 1].addCards(card2)
        self.hands[self.index + 1].wasSplit = True

    def _canAfford(self, ratioName):
        needed_amt = floor(self.pot * get(ratioName))
        return self.player.stack.amount >= needed_amt

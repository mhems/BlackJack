####################
#
# Table.py
#
####################

import src.Utilities.Configuration

from src.Basic.Shoe import Shoe
from src.Basic.Shoe import faro_shuffle
from src.Game.TableSlot import TableSlot
from src.Game.HouseBank import HouseBank

class Table:
    """Representation of Blackjack Table"""

    def __init__(self, num_slots = 6):
        """Initializes table members"""
        self.__dealer_slot = TableSlot()
        self.__bank        = HouseBank()
        self.__num_slots   = num_slots
        # Index 0 is dealer's leftmost slot
        self.__slots       = [TableSlot() for _ in xrange(self.__num_slots)]
        self.__shoe        = Shoe(Configuration.get('NUM_DECKS'),
                                  faro_shuffle,
                                  Configuration.get('CUT_INDEX'))
        self.__dealer_slot.seatPlayer(Dealer())

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
        return (slot for slot in self.slots if slot.isOccupied())

    @property
    def active_slots(self):
        """Returns generator for all slots with active players at table"""
        return (slot for slot in self.slots if slot.isActive())

    def register_player(self, player, pos=-1):
        """Register player to table, provided there is room"""
        if pos < 0:
            # Look from dealer's left to right for opening
            for slot in self.slots
                if not slot.isOccupied():
                    slot.seatPlayer(player)
                    return True
            return False
        elif pos > self.__num_slots:
            return False
        else:
            return self.__slots[pos].isOccupied()

    def play(self):
        """Plays one round of blackjack"""
        # Ask each seated player to bet
        for slot in self.occupied_slots():
            slot.promptBet()
        # Deal first card to each active player then dealer
        for slot in self.active_slots():
            slot.addCard(self.__shoe.dealOneCard())
        self.__dealer_slot.addCard(self.__shoe.dealOneCard())
        # Deal second card to each active player then dealer
        for slot in self.active_slots():
            slot.addCard(self.__shoe.dealOneCard())
        upcard = self.__shoe.dealOneCard()
        self.__dealer_slot.addCard(upcard)
        for slot in self.active_slots():
            slot.takeTurn(upcard)
        # pay out each player
        # clear hands

    def unregister_player(self, player):
        """Unregister player from table"""
        for pos, slot in self.occupied_slots:
            if slot.player == player:
                self.unregister_player_from_slot(pos)
                    
    def unregister_player_from_slot(self, pos):
        """Unregister player from slot, if present"""
        if self.__slots[pos].isOccupied():
            self.__slots[pos].unseatPlayer()

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
        return len(s for s in self.__slots if s.isActive())

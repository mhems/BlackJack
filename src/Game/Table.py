####################
#
# Table.py
#
####################

import src.Utilities.Configuration

class Table:
    """Representation of Blackjack Table"""

    def __init__(self, num_slots = 6):
        self.__dealer    = Dealer()
        self.__bank      = HouseBank()
        self.__num_slots = num_slots # tuple of (player, bet)
        self.__slots     = []
        self.__shoe      = Shoe(Configuration.configuration['NUM_DECKS'],
                                None, # FIX
                                Configuration.configuration['CUT_INDEX'])
        
        
    def register_player(self, player):
        """Register player to table, provided there is room"""
        pass

    def play(self):
        """Plays one round of blackjack"""
        pass

    def unregister_player(self, player):
        """Unregister player from table"""
        pass
    
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

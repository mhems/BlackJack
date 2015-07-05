####################
#
# Player.py
#
####################

class Player:
    """Representation of a blackjack player"""

    def __init__(self, name, action_policy):
        """Initializes Player members"""
        self.__stack      = ChipStack()
        self.name         = name
        self.__hands      = []
        self.__hand_index = 0
        self.__isActive   = False
        self.__policy     = action_policy

    @property
    def stackAmount(self):
        """Returns amount of chips in player's stack"""
        return self.__stack.amount
        
    def wager(self, amt):
        """Attempts to wager amt"""
        pass

    def receive_payment(self, amt):
        """Adds amt to chip stack"""
        pass
    
    def act(self, upcard):
        """Returns command player wishes to execute based on its policy"""
        return self.__policy.act(self.hands[self.__hand_index], upcard)

    def __eq__(self, other):
        """Returns True iff player is other"""
        return self.id == other.id

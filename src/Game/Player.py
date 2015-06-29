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
        
    def wager(self, amt):
        """Attempts to wager amt"""
        pass

    def receive_payment(self, amt):
        """Adds amt to chip stack"""
        pass

    def receiveCard(self, card):
        self.__hands[self.__hand_index].addCards(card)

    def act(self, upcard):
        return self.__policy.act(self.hands[self.__hand_index], upcard)

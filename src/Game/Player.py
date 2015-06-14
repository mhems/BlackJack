####################
#
# Player.py
#
####################

class Player:
    """Representation of a blackjack player"""

    def __init__(self, name):
        """Initializes Player members"""
        self.__stack      = ChipStack()
        self.name         = name
        self.__hands      = []
        self.__hand_index = 0
        self.__isActive   = False
        
    def wager(self, amt):
        """Attempts to wager amt"""
        pass

    def receive_payment(self, amt):
        """Adds amt to chip stack"""
        pass

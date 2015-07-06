####################
#
# Player.py
#
####################

from src.Game.ChipStack import ChipStack

class Player:
    """Representation of a blackjack player"""

    def __init__(self, name, policy, betting_policy):
        """Initializes Player members"""
        self.__stack      = ChipStack()
        self.name         = name
        self.__hands      = []
        self.__hand_index = 0
        self.__isActive   = False
        self.__policy     = policy
        self.__bet_policy = betting_policy

    @property
    def stackAmount(self):
        """Returns amount of chips in player's stack"""
        return self.__stack.amount
        
    def wager(self, amt):
        """Attempts to wager amt"""
        return self.__stack.withdraw(amt)

    def receive_payment(self, amt):
        """Adds amt to chip stack"""
        self.__stack.deposit(amt)
    
    def act(self, hand, upcard, availableCommands):
        """Returns command player wishes to execute based on its policy"""
        return self.__policy.decide(hand, upcard, availableCommands)

    def bet(self):
        """Returns amount player wishes to bet"""
        return self.__bet_policy.bet()
    
    def __eq__(self, other):
        """Returns True iff player is other"""
        return id(self) == id(other)

    def __str__(self):
        """Returns string representation of player"""
        return '%s has $%d' % (self.name, self.stackAmount)

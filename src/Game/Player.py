####################
#
# Player.py
#
####################

from src.Game.ChipStack import ChipStack

class Player:
    """Representation of a blackjack player"""

    def __init__(self, name, decision_policy, insurance_policy, betting_policy):
        """Initializes Player members"""
        self.__stack            = ChipStack()
        self.name               = name
        self.__hands            = []
        self.__hand_index       = 0
        self.__isActive         = False
        self.__decision_policy  = decision_policy
        self.__insurance_policy = insurance_policy
        self.__bet_policy       = betting_policy

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
    
    def act(self, hand, upcard, availableCommands, **kwargs):
        """Returns command player wishes to execute based on its policy"""
        return self.__decision_policy.decide(hand, upcard, availableCommands, **kwargs)

    def insure(self, hand, **kwargs):
        """Returns True iff player wishes to insure based on its policy"""
        return self.__insurance_policy.insure(hand, **kwargs)

    def bet(self):
        """Returns amount player wishes to bet"""
        return self.__stack.withdraw(self.__bet_policy.bet())
    
    def __eq__(self, other):
        """Returns True iff player is other"""
        return id(self) == id(other)

    def __str__(self):
        """Returns string representation of player"""
        return '%s has $%d' % (self.name, self.stackAmount)

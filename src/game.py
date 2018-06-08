from policies import (DealerPolicy, DeclineInsurancePolicy)

class InsufficientFundsError(Exception):
    """Error class to represent error of overwithdrawing from bank"""

    def __init__(self, request, balance):
        super().__init__()
        self.request = request
        self.balance = balance

    def __str__(self):
        return 'Insufficient funds to withdraw $%s from $%s' % (self.request,
                                                                self.balance)

class Bank:
    """Model for withdraw/deposit transactions"""

    def __init__(self):
        """Initializes Bank"""
        self.amount = 0

    def withdraw(self, amt):
        """Attempts to withdraw amt from Bank.
        If there is less than amt in the Bank, raises InsufficientFundsError"""
        if amt > self.amount:
            raise InsufficientFundsError(amt, self.amount)
        self.amount -= amt
        return amt

    def deposit(self, amt):
        """Deposits amt into Bank"""
        if amt < 0:
            raise ValueError('amt cannot be negative')
        self.amount += amt

class HouseBank(Bank):
    """Model for endless Bank"""

    def __init__(self):
        """Initializes HouseBank"""
        super().__init__()

    def withdraw(self, amt):
        """Withdraws amt from Bank"""
        self.amount -= amt
        return amt


class Player:
    """Representation of a blackjack player"""

    def __init__(self,
                 name,
                 decision_policy=None,
                 insurance_policy=None,
                 betting_policy=None):
        """Initializes Player members"""
        self.stack = Bank()
        self.name = name
        self.hands = []
        self.hand_index = 0
        self.isActive = False
        self.decision_policy = decision_policy
        self.insurance_policy = insurance_policy
        self.bet_policy = betting_policy

    def wager(self, amt):
        """Attempts to wager amt"""
        return self.stack.withdraw(amt)

    def receive_payment(self, amt):
        """Adds amt to chip stack"""
        self.stack.deposit(amt)

    def act(self, hand, upcard, availableCommands, **kwargs):
        """Returns command player wishes to execute based on its policy"""
        return self.decision_policy.decide(hand,
                                           upcard,
                                           availableCommands,
                                           **kwargs)

    def insure(self, hand, **kwargs):
        """Returns True iff player wishes to insure based on its policy"""
        return self.insurance_policy.insure(hand, **kwargs)

    def amountToBet(self, **kwargs):
        """Returns amount player wishes to bet"""
        return self.bet_policy.bet(**kwargs)

    def __eq__(self, other):
        """Returns True iff player is other"""
        return id(self) == id(other)

    def __str__(self):
        """Returns string representation of player"""
        return '%s ($%d)' % (self.name, self.stack.amount)

class Dealer(Player):
    """Representation of blackjack dealer"""

    def __init__(self, name='Dealer'):
        """Initializes Dealer members"""
        super().__init__(name, DealerPolicy(), DeclineInsurancePolicy())
        self.isActive = True

    def amountToBet(self, **kwargs):
        """Dealer does not bet"""
        return 0

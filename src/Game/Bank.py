class InsufficientFundsError(Exception):
    """Error class to represent error of overwithdrawing from bank"""

    def __init__(self, request, balance):
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

from src.Basic.Card import Card

class Event():
    """Base class for all Events"""
    pass

class ShoeEvent(Event):
    """Base class for all Shoe Events"""
    pass

class DealEvent(ShoeEvent):
    """Class for deal events"""

    def __init__(self, card, visible):
        self.card = card
        self.visible = visible

class BurnEvent(ShoeEvent):
    """Class for burn events"""
    pass

class ShuffleEvent(ShoeEvent):
    """Class for shuffle events"""
    pass

class BankEvent(Event):
    """Base class for bank events"""
    pass

class WithdrawEvent(BankEvent):
    """Class for withdrawal events"""
    pass

class DepositEvent(BankEvent):
    """Class for deposit events"""
    pass

class BettingEvent(Event):
    """Class for bet events"""

    def __init__(self, amt):
        self.amount = amt

class InsuranceEvent(Event):
    """Class for insurance events"""

    def __init__(self, amt):
        self.amount = amt

class DecisionEvent(Event):
    """Class for decision events"""

    def __init__(self, decision):
        self.decision = decision

class CommandEvent(Event):
    """Class for command events"""

    def __init__(self, cmd):
        self.command = cmd

class HitEvent(CommandEvent):
    """Class for Hit events"""

    def __init__(self, card):
        self.card = card

# ... ?

if __name__ == '__main__':
    s = DealEvent(Card(4,'H'), True)
    print(s.card)
    b = BurnEvent()

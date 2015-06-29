####################
#
# DealerAction.py
#
####################

class DealerAction(Action):
    """Class for blackjack Dealer's action policy"""

    def act(self, hand, _):
        """Acts according to dealer rules"""
        if hand.value() < 17:
            return Command.HIT
        elif hand.value() > 17:
            return Command.STAND
        else:
            if hand.hasAce():
                if Configuration.get('DEALER_HITS_ON_SOFT_17'):
                    return Command.HIT
                else:
                    return Command.STAND
            else:
                return Command.STAND

####################
#
# HumanInputAction.py
#
####################

class HumanInputAction(Action):
    """Class to prompt human for action policy"""

    __allowed_inputs = ['H', 'S', 'SP', 'D', 'SU', 'ES']
    
    def act(self, hand, upcard):
        """ACts according to human input"""
        action = input('Your hand (%s) has value %d, Dealer shows %s' % (hand, hand.value(), upcard))
        while action.upper() not in __allowed_inputs():
            print('Unknown action: %s' % action)
            action = input('Your hand (%s) has value %d, Dealer shows %s' % (hand, hand.value(), upcard))
        return Command.command_map[action.upper()]

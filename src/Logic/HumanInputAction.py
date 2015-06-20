####################
#
# HumanInputAction.py
#
####################

class HumanInputAction(Action):
    """Class to prompt human for action policy"""

    __allowed_inputs = ['H', 'S', 'SP', 'D', 'SU', 'ES']
    
    def act(self, hand, upcard):
        """Acts according to human input"""
        print('Your hand (%s) has value %d, Dealer shows %s' % (hand, hand.value(), upcard))
        action = input('How will you act? Options = %s\n' % __allowed_inputs)
        while action.upper() not in __allowed_inputs():
            print('Unknown action: %s' % action)
            action = input('How will you act? Options = %s\n' % __allowed_inputs)
        return Command.getCommand(action.upper())

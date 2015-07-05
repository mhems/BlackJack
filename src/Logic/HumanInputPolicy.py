####################
#
# HumanInputPolicy.py
#
####################

from src.Logic.Command        import Command
from src.Logic.DecisionPolicy import DecisionPolicy

class HumanInputPolicy(DecisionPolicy):
    """Class to prompt human for decision"""

    def decide(self, hand, upcard, availableCommands, **kwargs):
        """Decides according to human input"""

        def __prompt(self, availableCommands):
            """Prompts for response"""
            response = input('How will you act? Options = %s\n' %
                             (', '.join((str(c) for c in availableCommands))))
            return Command.getCommand(response), response

        print('Your hand (%s) has value %d, Dealer shows %s' % (hand,
                                                                hand.value,
                                                                upcard))
        command, response = self.__prompt(availableCommands)
        while not command:
            print('Unknown or unavailable action: %s' % response)
            command, response = self.__prompt(availableCommands)
        return command

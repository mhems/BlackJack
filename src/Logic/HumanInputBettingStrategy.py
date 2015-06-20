####################
#
# HumanInputBettingStrategy.py
#
####################

class HumanInputBettingStrategy(BettingStrategy):
    """Policy to bet based on inputted amount"""

    def bet(self):
        """Bets according to human input"""
        result = input('Enter your bet amount: ')
        while not re.match(r'[1-9][0-9]+', result):
            print('Bet must be positive integer')
            result =input('Enter your bet amount: ')
        return result

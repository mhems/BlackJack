from abc import ABCMeta, abstractmethod
import re

from src.Logic.Command import Command
from src.Basic.Card import Card
import src.Utilities.Configuration as config

class DecisionPolicy(metaclass=ABCMeta):
    """Base class for decision policies on how to act"""

    @abstractmethod
    def decide(self, hand, upcard, availableCommands, **kwargs):
        """Returns Command that policy wishes to execute"""
        raise NotImplementedError(
            'DecisionPolicy implementations must implement the act method')

class BasicStrategyPolicy(DecisionPolicy):
    """Represents use of basic strategy to inform actions"""

    def __init__(self, filename):
        self.strategy = StrategyChart.fromFile(filename)

    def decide(self, hand, upcard, availableCommands, **kwargs):
        """Decides command based on basic strategy"""
        upvalue = 'A' if upcard.isAce else upcard.value
        return self.strategy.advise(hand, upvalue, availableCommands)

class DealerPolicy(DecisionPolicy):
    """Class for blackjack Dealer's decision policy"""

    def decide(self, hand, upcard, _, **kwargs):
        """Decides command according to dealer rules"""
        hitS17 = hand.isSoft17 and config.get('DEALER_HITS_ON_SOFT_17')
        if hand.value < 17 or hitS17:
            return Command.HIT
        return Command.STAND

class FeedbackDecisionPolicy(DecisionPolicy):
    """Represents use of human input with basic strategy
       used to advise player after decision"""

    def __init__(self, input_policy, strategy_policy):
        """Initializes members"""
        self.input_policy = input_policy
        self.strategy_policy = strategy_policy
        self.num_wrong = 0

    def decide(self, hand, upcard, availableCommands, **kwargs):
        """First corrects player's decision if wrong, then
           returns Command that policy wishes to execute"""
        decision = self.input_policy.decide(hand,
                                            upcard,
                                            availableCommands,
                                            **kwargs)
        expected = self.strategy_policy.decide(hand,
                                               upcard,
                                               availableCommands,
                                               **kwargs)
        if decision != expected and expected in availableCommands:
            self.num_wrong += 1
            print('WRONG: You %s when you should have %s' %
                  (Command.command_to_past_tense[decision],
                    Command.command_to_past_tense[expected]))
        return decision

class HumanInputPolicy(DecisionPolicy):
    """Class to prompt human for decision"""



    def decide(self, hand, upcard, availableCommands, **kwargs):
        """Decides according to human input"""

        def prompt(availableCommands):
            """Prompts for response"""
            response = input('How will you act? Options = %s\n' %
                             ', '.join(Command.command_to_string[e] for e in availableCommands))
            if response.upper() in Command.string_to_command:
                return True, response
            return False, None

        print('Your hand (%s) has value %d, Dealer shows %s' % (hand.ranks,
                                                                hand.value,
                                                                upcard))
        success, response = prompt(availableCommands)
        while not success:
            print('Unknown or unavailable action: %s' % response)
            success, response = prompt(availableCommands)
        return Command.string_to_command[response.upper()]

class StrategyChart:
    """Mechanism for strategy advice"""

# Actions:
# H  - Hit
# S  - Stand
# Sp - Split
# Ds - Double,    stand if not allowed
# Dh - Double,    hit   if not allowed
# Su - Surrender, hit   if not allowed

    class Chart:
        """Representation of advice chart"""

        def __init__(self, chart):
            self.chart = chart

        @staticmethod
        def fromFileContents(lines):
            """Create Chart from file contents"""
            chart = {}
            index = 0
            for line in lines:
                if re.match(r'^[ \t]*>', line):
                    break
                toks = re.split(r'[ |,\t\r\n]+', line, flags=re.I)
                if not toks:
                    pass # signal error
                toks = [t for t in toks if len(t) > 0]
                player_val = toks[0]
                if re.match(r'\b[12]?[0-9]\b', player_val):
                    player_val = int(player_val)
                for (card, action) in zip(Card.values, toks[1:]):
                    chart[(player_val, card)] = action
                index += 1
            return StrategyChart.Chart(chart), index

        def access(self, value, upcard):
            """Accesses chart entry at the value row and upcard column"""
            if (value, upcard) in self.chart:
                return self.chart[(value, upcard)]
            return None

        def __len__(self):
            return len(self.chart)

        def __repr__(self):
            """Returns string representation of chart"""

            def sort(value):
                """Function to sort card rank characters"""
                return value if value != 'A' else Card.HARD_ACE_VALUE

            fmt = '#    %s' + '\n'
            result = fmt % ' '.join(( str(e).rjust(2, ' ')
                                      for e in Card.values ))
            vals = sorted(set(t[0] for t in self.chart.keys()),
                          key = sort,
                          reverse = True)
            fmt = ' %s  %s' + '\n'
            for value in vals:
                result += fmt % (str(value).rjust(2, ' '),
                                 ' '.join(str(self.chart[(value, up)]).rjust(2, ' ')
                                          for up in Card.values))
            return result

    # END CHART CLASS

    def __init__(self, hard_chart, soft_chart, pair_chart):
        self.hard_chart = hard_chart
        self.soft_chart = soft_chart
        self.pair_chart = pair_chart

    @staticmethod
    def fromFile(filename):
        """Create StrategyChart from file"""
        def hasContent(line):
            return not (re.match(r'^[ \t]*$', line) or
                        re.match(r'^[ \t]*#', line))
        File = open(filename, 'r')
        lines = [line.rstrip() for line in File.readlines() if hasContent(line)]
        hard_chart = None
        soft_chart = None
        pair_chart = None
        fromFileContents = StrategyChart.Chart.fromFileContents
        while len(lines) > 0:
            line = lines[0]
            if re.match(r'^[ \t]*>', line):
                if re.search(r'hard', line, re.I):
                    hard_chart, index = fromFileContents(lines[1:])
                    lines = lines[index+1:]
                elif re.search(r'soft', line, re.I):
                    soft_chart, index = fromFileContents(lines[1:])
                    lines = lines[index+1:]
                elif re.search(r'pair', line, re.I):
                    pair_chart, index = fromFileContents(lines[1:])
                    lines = lines[index+1:]
                else:
                    print('Unknown line: %s' % line)
            else:
                print('Unknown line: %s' % line)
        File.close()
        return StrategyChart(hard_chart, soft_chart, pair_chart)

    def advise(self, player_hand, dealer_up_card, availableCommands):
        """Advise action given player's hand and dealer's up card"""
        value = player_hand.value
        advice = None
        if config.get('SPLIT_BY_VALUE'):
            isPair = player_hand.isPairByValue
        else:
            isPair = player_hand.isPairByRank
        # check for pair
        if isPair and self.pair_chart:
            arg = 'A' if player_hand.hasAce else int(value/2)
            advice = self.pair_chart.access(arg, dealer_up_card)
            if advice == 'Sp' and Command.SPLIT not in availableCommands:
                # defer iff split advised but unavailable
                advice = None
        # check for soft
        if not advice and player_hand.isSoft and self.soft_chart:
            advice = self.soft_chart.access(value, dealer_up_card)
        # default to hard
        if not advice and self.hard_chart:
            advice = self.hard_chart.access(value, dealer_up_card)
        if advice:
            if advice[0].upper() == 'D' and len(advice) == 2:
                if Command.DOUBLE in availableCommands:
                    return Command.DOUBLE
                elif advice[1].upper() == 'H':
                    return Command.HIT
                elif advice[1].upper() == 'S':
                    return Command.STAND
            elif ( advice.upper() == 'SU' and
                   Command.SURRENDER not in availableCommands):
                return Command.HIT
            return Command.string_to_command[advice.upper()]
        return None

    def toFile(self, filename):
        """Writes chart(s) to file in parse-expected format"""
        pass

    def __repr__(self):
        result = ''
        if len(self.hard_chart) > 0:
            result += '> Hard totals' + '\n'
            result += repr(self.hard_chart)
        if len(self.soft_chart) > 0:
            result += '\n\n> Soft totals\n'
            result += repr(self.soft_chart)
        if len(self.pair_chart) > 0:
            result += '\n\n> Pairs\n'
            result += repr(self.pair_chart)
        return result

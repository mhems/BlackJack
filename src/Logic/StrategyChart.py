####################
#
# StrategyChart.py
#
####################

import re

from src.Utilities.Configuration import Configuration
from src.Basic.BlackjackHand     import BlackjackHand
from src.Basic.Card              import Card

# Actions:
# H  - Hit
# S  - Stand
# Sp - Split
# Ds - Double, stand if not allowed
# Dh - Double, hit if not allowed
# Su - Surrender, hit if not allowed

class StrategyChart:
    """Mechanism for strategy advice"""

    class Chart:
        """Representation of advice chart"""

        def __init__(self, chart):
            self.__chart = chart

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
            return chart[(value, upcard)] if (value, upcard) in chart else None

        def __len__(self):
            return len(self.__chart)

        def __repr__(self):
            """Returns string representation of chart"""
            result = '#    %s\n' % ' '.join(str(e).rjust(2,' ') for e in Card.values)
            vals = sorted(set(t[0] for t in self.__chart.keys()),
                          key = lambda value: value if value != 'A' else Card.HARD_ACE_VALUE,
                          reverse=True)
            for value in vals:
                result += ' %s  %s\n' % (str(value).rjust(2, ' '),
                                         ' '.join(str(self.__chart[(value, up)]).rjust(2, ' ') for up in Card.values))
            return result

    # END CHART CLASS
                
    def __init__(self, hard_chart, soft_chart, pair_chart):
        self.__hard_chart = hard_chart
        self.__soft_chart = soft_chart
        self.__pair_chart = pair_chart
        
    @staticmethod
    def fromFile(filename):
        """Create StrategyChart from file"""
        def hasContent(line):
            return not (re.match(r'^[ \t]*$', line) or
                        re.match(r'^[ \t]*#', line))
        File = open(filename, 'r')
        lines = [line.rstrip() for line in File.readlines() if hasContent(line)]
        hard_chart = {}
        soft_chart = {}
        pair_chart = {}
        while len(lines) > 0:
            line = lines[0]
            if re.match(r'^[ \t]*>', line):
                if re.search(r'hard', line, re.I):
                    hard_chart, index = StrategyChart.Chart.fromFileContents(lines[1:])
                    lines = lines[index+1:]
                elif re.search(r'soft', line, re.I):
                    soft_chart, index = StrategyChart.Chart.fromFileContents(lines[1:])
                    lines = lines[index+1:]
                elif re.search(r'pair', line, re.I):
                    pair_chart, index = StrategyChart.Chart.fromFileContents(lines[1:])
                    lines = lines[index+1:]
                else:
                    print('Unknown line: %s' % line)
            else:
                print('Unknown line: %s' % line)
        File.close()
        return StrategyChart(hard_chart, soft_chart, pair_chart)
        
    def advise(self, player_hand, dealer_up_card):
        """Advise action given player's hand and dealer's up card"""
        value = player_hand.value()
        if Configuration.configuration['SPLIT_BY_VALUE']:
            func = player_hand.isPairByValue
        else:
            func = player_hand.isPairByRank
        # check for pair
        if func():
            arg = 'A' if player_had.hasAce() else value/2
            advice = self.__pair_chart.access('A', dealer_up_card)
            if advice:
                return advice
        # check for soft
        if player_hand.hasAce():
            advice = self.__soft_chart.access(value, dealer_up_card)
            if advice:
                return advice
        # default to hard    
        return self.__hard_chart.access(value, dealer_up_card)

    def toFile(self, filename):
        """Writes chart(s) to file in parse-expected format"""
        File = open(filename, 'w')

    def __repr__(self):
        result = ''
        if len(self.__hard_chart) > 0:
            result += '> Hard totals\n'
            result += repr(self.__hard_chart)
        if len(self.__soft_chart) > 0:
            result += '\n\n'
            result += '> Soft totals\n'
            result += repr(self.__soft_chart)
        if len(self.__pair_chart) > 0:
            result += '\n\n'
            result += '> Pairs\n'
            result += repr(self.__pair_chart)
        return result

sc = StrategyChart.fromFile('three_chart.txt')
print(repr(sc))
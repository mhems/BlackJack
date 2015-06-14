####################
#
# StrategyChart.py
#
####################

import re

from src.Utilities.Configuration import Configuration
from src.Basic.BlackjackHand     import BlackjackHand

# Actions:
# H  - Hit
# S  - Stand
# Sp - Split
# Ds - Double, stand if not allowed
# Dh - Double, hit if not allowed
# Su - Surrender, hit if not allowed


class StrategyChart:
    """Mechanism for strategy advice"""
    
    def __init__(self, hard_chart, soft_chart, pair_chart):
        self.__hard_chart = hard_chart
        self.__soft_chart = soft_chart
        self.__pair_chart = pair_chart
        
    @staticmethod
    def fromFile(filename):
        """Create StrategyChart from file"""
        values = [2,3,4,5,6,7,8,9,10,'A']
        value_re = r'\b[12]?[0-9]\b'
        File = open(filename, 'r')
        hard_chart = {}
        soft_chart = {}
        pair_chart = {}
        for line in File.readlines():
            if re.match(r'^[ \t]*$', line):
                continue
            if re.match(r'^[ \t]*#', line):
                continue
            if re.match(r'^[ \t]*>', line):
                if re.search(r'hard', line, re.I):
                    current_chart = hard_chart
                elif re.search(r'soft', line, re.I):
                    current_chart = soft_chart
                elif re.search(r'pair', line, re.I):
                    current_chart = pair_chart
                continue
            toks = re.split(r'[ |,\t\r\n]+', line, flags=re.I)
            if not toks:
                pass # signal error
            toks = [t for t in toks if len(t) > 0]
            player_val = toks[0]
            if re.match(value_re, player_val):
                player_val = int(player_val)
            for (card, action) in zip(values, toks[1:]):
                current_chart[(player_val, card)] = action
        File.close()
        return StrategyChart(hard_chart, soft_chart, pair_chart)
        
    def advise(self, player_hand, dealer_up_card):
        """Advise action given player's hand and dealer's up card"""

        access = lambda chart, value, upcard: chart[(value, upcard)] if (value, upcard) in chart else None
        value = player_hand.value()

        if Configuration.configuration['SPLIT_BY_VALUE']:
            func = player_hand.isPairByValue
        else:
            func = player_hand.isPairByRank
        # check for pair
        if func():
            if player_hand.hasAce():
                advice = access(self.__pair_chart, 'A', dealer_up_card)
            else:
                advice = access(self.__pair_chart, value/2, dealer_up_card)
            if advice:
                return advice
        if player_hand.hasAce():
            # check for soft
            advice = access(self.__soft_chart, value, dealer_up_card)
            if advice:
                return advice
        return access(self.__hard_chart, value, dealer_up_card)

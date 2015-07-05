####################
#
# testStrategyChart.py
#
####################

import re
import unittest

from src.Logic.StrategyChart import StrategyChart
from src.Basic.BlackjackHand import BlackjackHand
from src.Basic.Card          import Card
from src.Logic.Command       import Command

class testStrategyChart(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def assertRow(self, chart, hand, exp):
        ls = re.split(r' +', exp)
        for (up, e) in zip(Card.values, ls):
            advise = chart.advise(hand, up)
            expect = Command.getCommand(e)
            self.assertEqual(advise, expect,
                             'Hand %s vs %s: Expected %s; Got %s' % (hand,
                                                                     up,
                                                                     expect,
                                                                     advise))

    def testThreeCompleteCharts(self):
        chart = StrategyChart.fromFile('tests/Logic/test_files/three_chart.txt')

        # test pair advice
        hand = makePair('A')
        self.assertRow(chart, hand, 'Sp Sp Sp Sp Sp Sp Sp Sp Sp Sp')
        hand = makePair(10)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makePair(9)
        self.assertRow(chart, hand, 'Sp Sp Sp Sp Sp S Sp Sp S S')
        hand = makePair(8)
        self.assertRow(chart, hand, 'Sp Sp Sp Sp Sp Sp Sp Sp Sp Sp')
        hand = makePair(7)
        self.assertRow(chart, hand, 'Sp Sp Sp Sp Sp Sp H H H H')
        hand = makePair(6)
        self.assertRow(chart, hand, 'Sp Sp Sp Sp Sp H H H H H')
        hand = makePair(5)
        self.assertRow(chart, hand, 'Dh Dh Dh Dh Dh Dh Dh Dh H H')
        hand = makePair(4)
        self.assertRow(chart, hand, 'H H H Sp Sp H H H H H')
        hand = makePair(3)
        self.assertRow(chart, hand, 'Sp Sp Sp Sp Sp Sp H H H H')
        hand = makePair(2)
        self.assertRow(chart, hand, 'Sp Sp Sp Sp Sp Sp H H H H')

        # test soft advice
        hand = makeSoft(9)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeSoft(8)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeSoft(7)
        self.assertRow(chart, hand, 'S Ds Ds Ds Ds S S H H H')
        hand = makeSoft(6)
        self.assertRow(chart, hand, 'H Dh Dh Dh Dh H H H H H')
        hand = makeSoft(5)
        self.assertRow(chart, hand, 'H H Dh Dh Dh H H H H H')
        hand = makeSoft(4)
        self.assertRow(chart, hand, 'H H Dh Dh Dh H H H H H')
        hand = makeSoft(3)
        self.assertRow(chart, hand, 'H H H Dh Dh H H H H H')
        hand = makeSoft(2)
        self.assertRow(chart, hand, 'H H H Dh Dh H H H H H')

        # test hard advice
        hand = makeHand(10,10)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeHand(10, 9)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeHand(10, 8)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeHand(10, 7)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeHand(10, 6)
        self.assertRow(chart, hand, 'S S S S S H H Su Su Su')
        hand = makeHand(10, 5)
        self.assertRow(chart, hand, 'S S S S S H H H Su H')
        hand = makeHand(10, 4)
        self.assertRow(chart, hand, 'S S S S S H H H H H')
        hand = makeHand(10, 3)
        self.assertRow(chart, hand, 'S S S S S H H H H H')
        hand = makeHand(10, 2)
        self.assertRow(chart, hand, 'H H S S S H H H H H')
        hand = makeHand( 2, 9)
        self.assertRow(chart, hand, 'Dh Dh Dh Dh Dh Dh Dh Dh Dh H')
        hand = makeHand( 2, 8)
        self.assertRow(chart, hand, 'Dh Dh Dh Dh Dh Dh Dh Dh H H')
        hand = makeHand( 2, 7)
        self.assertRow(chart, hand, 'H Dh Dh Dh Dh H H H H H')
        hand = makeHand( 2, 6)
        self.assertRow(chart, hand, 'H H H H H H H H H H')
        hand = makeHand( 2, 5)
        self.assertRow(chart, hand, 'H H H H H H H H H H')
        hand = makeHand( 2, 4)
        self.assertRow(chart, hand, 'H H H H H H H H H H')
        hand = makeHand( 2, 3)
        self.assertRow(chart, hand, 'H H H H H H H H H H')

    def testNoPairCharts(self):
        chart = StrategyChart.fromFile('tests/Logic/test_files/no_pair.txt')

        # test pair -- should be same as advice for sum
        hand = makePair('A')
        self.assertRow(chart, hand, 'H H S S S H H H H H')
        hand = makePair(10)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makePair(9)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makePair(8)
        self.assertRow(chart, hand, 'S S S S S H H Su Su Su')
        hand = makePair(7)
        self.assertRow(chart, hand, 'S S S S S H H H H H')
        hand = makePair(6)
        self.assertRow(chart, hand, 'H H S S S H H H H H')
        hand = makePair(5)
        self.assertRow(chart, hand, 'Dh Dh Dh Dh Dh Dh Dh Dh H H')
        hand = makePair(4)
        self.assertRow(chart, hand, 'H H H H H H H H H H')
        hand = makePair(3)
        self.assertRow(chart, hand, 'H H H H H H H H H H')
        hand = makePair(2)
        self.assertRow(chart, hand, 'H H H H H H H H H H')
        
        # test soft advice
        hand = makeSoft(9)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeSoft(8)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeSoft(7)
        self.assertRow(chart, hand, 'S Ds Ds Ds Ds S S H H H')
        hand = makeSoft(6)
        self.assertRow(chart, hand, 'H Dh Dh Dh Dh H H H H H')
        hand = makeSoft(5)
        self.assertRow(chart, hand, 'H H Dh Dh Dh H H H H H')
        hand = makeSoft(4)
        self.assertRow(chart, hand, 'H H Dh Dh Dh H H H H H')
        hand = makeSoft(3)
        self.assertRow(chart, hand, 'H H H Dh Dh H H H H H')
        hand = makeSoft(2)
        self.assertRow(chart, hand, 'H H H Dh Dh H H H H H')

        # test hard advice
        hand = makeHand(10,10)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeHand(10, 9)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeHand(10, 8)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeHand(10, 7)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeHand(10, 6)
        self.assertRow(chart, hand, 'S S S S S H H Su Su Su')
        hand = makeHand(10, 5)
        self.assertRow(chart, hand, 'S S S S S H H H Su H')
        hand = makeHand(10, 4)
        self.assertRow(chart, hand, 'S S S S S H H H H H')
        hand = makeHand(10, 3)
        self.assertRow(chart, hand, 'S S S S S H H H H H')
        hand = makeHand(10, 2)
        self.assertRow(chart, hand, 'H H S S S H H H H H')
        hand = makeHand( 2, 9)
        self.assertRow(chart, hand, 'Dh Dh Dh Dh Dh Dh Dh Dh Dh H')
        hand = makeHand( 2, 8)
        self.assertRow(chart, hand, 'Dh Dh Dh Dh Dh Dh Dh Dh H H')
        hand = makeHand( 2, 7)
        self.assertRow(chart, hand, 'H Dh Dh Dh Dh H H H H H')
        hand = makeHand( 2, 6)
        self.assertRow(chart, hand, 'H H H H H H H H H H')
        hand = makeHand( 2, 5)
        self.assertRow(chart, hand, 'H H H H H H H H H H')
        hand = makeHand( 2, 4)
        self.assertRow(chart, hand, 'H H H H H H H H H H')
        hand = makeHand( 2, 3)
        self.assertRow(chart, hand, 'H H H H H H H H H H')


    def testNoSoft(self):
        chart = StrategyChart.fromFile('tests/Logic/test_files/no_soft.txt')

        # test soft -- should be same as for sum
        hand = makeSoft(9)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeSoft(8)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeSoft(7)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeSoft(6)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeSoft(5)
        self.assertRow(chart, hand, 'S S S S S H H Su Su Su')
        hand = makeSoft(4)
        self.assertRow(chart, hand, 'S S S S S H H H Su H')
        hand = makeSoft(3)
        self.assertRow(chart, hand, 'S S S S S H H H H H')
        hand = makeSoft(2)
        self.assertRow(chart, hand, 'S S S S S H H H H H')

        # test pair advice
        hand = makePair('A')
        self.assertRow(chart, hand, 'Sp Sp Sp Sp Sp Sp Sp Sp Sp Sp')
        hand = makePair(10)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makePair(9)
        self.assertRow(chart, hand, 'Sp Sp Sp Sp Sp S Sp Sp S S')
        hand = makePair(8)
        self.assertRow(chart, hand, 'Sp Sp Sp Sp Sp Sp Sp Sp Sp Sp')
        hand = makePair(7)
        self.assertRow(chart, hand, 'Sp Sp Sp Sp Sp Sp H H H H')
        hand = makePair(6)
        self.assertRow(chart, hand, 'Sp Sp Sp Sp Sp H H H H H')
        hand = makePair(5)
        self.assertRow(chart, hand, 'Dh Dh Dh Dh Dh Dh Dh Dh H H')
        hand = makePair(4)
        self.assertRow(chart, hand, 'H H H Sp Sp H H H H H')
        hand = makePair(3)
        self.assertRow(chart, hand, 'Sp Sp Sp Sp Sp Sp H H H H')
        hand = makePair(2)
        self.assertRow(chart, hand, 'Sp Sp Sp Sp Sp Sp H H H H')

        # test hard advice
        hand = makeHand(10,10)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeHand(10, 9)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeHand(10, 8)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeHand(10, 7)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeHand(10, 6)
        self.assertRow(chart, hand, 'S S S S S H H Su Su Su')
        hand = makeHand(10, 5)
        self.assertRow(chart, hand, 'S S S S S H H H Su H')
        hand = makeHand(10, 4)
        self.assertRow(chart, hand, 'S S S S S H H H H H')
        hand = makeHand(10, 3)
        self.assertRow(chart, hand, 'S S S S S H H H H H')
        hand = makeHand(10, 2)
        self.assertRow(chart, hand, 'H H S S S H H H H H')
        hand = makeHand( 2, 9)
        self.assertRow(chart, hand, 'Dh Dh Dh Dh Dh Dh Dh Dh Dh H')
        hand = makeHand( 2, 8)
        self.assertRow(chart, hand, 'Dh Dh Dh Dh Dh Dh Dh Dh H H')
        hand = makeHand( 2, 7)
        self.assertRow(chart, hand, 'H Dh Dh Dh Dh H H H H H')
        hand = makeHand( 2, 6)
        self.assertRow(chart, hand, 'H H H H H H H H H H')
        hand = makeHand( 2, 5)
        self.assertRow(chart, hand, 'H H H H H H H H H H')
        hand = makeHand( 2, 4)
        self.assertRow(chart, hand, 'H H H H H H H H H H')
        hand = makeHand( 2, 3)
        self.assertRow(chart, hand, 'H H H H H H H H H H')

    def testOneChart(self):
        chart = StrategyChart.fromFile('tests/Logic/test_files/one_chart.txt')
        
        # test hard advice
        hand = makeHand(10,10)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeHand(10, 9)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeHand(10, 8)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeHand(10, 7)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeHand(10, 6)
        self.assertRow(chart, hand, 'S S S S S H H Su Su Su')
        hand = makeHand(10, 5)
        self.assertRow(chart, hand, 'S S S S S H H H Su H')
        hand = makeHand(10, 4)
        self.assertRow(chart, hand, 'S S S S S H H H H H')
        hand = makeHand(10, 3)
        self.assertRow(chart, hand, 'S S S S S H H H H H')
        hand = makeHand(10, 2)
        self.assertRow(chart, hand, 'H H S S S H H H H H')
        hand = makeHand( 2, 9)
        self.assertRow(chart, hand, 'Dh Dh Dh Dh Dh Dh Dh Dh Dh H')
        hand = makeHand( 2, 8)
        self.assertRow(chart, hand, 'Dh Dh Dh Dh Dh Dh Dh Dh H H')
        hand = makeHand( 2, 7)
        self.assertRow(chart, hand, 'H Dh Dh Dh Dh H H H H H')
        hand = makeHand( 2, 6)
        self.assertRow(chart, hand, 'H H H H H H H H H H')
        hand = makeHand( 2, 5)
        self.assertRow(chart, hand, 'H H H H H H H H H H')
        hand = makeHand( 2, 4)
        self.assertRow(chart, hand, 'H H H H H H H H H H')
        hand = makeHand( 2, 3)
        self.assertRow(chart, hand, 'H H H H H H H H H H')

        # test soft advice -- should be same
        hand = makeSoft(9)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeSoft(8)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeSoft(7)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeSoft(6)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makeSoft(5)
        self.assertRow(chart, hand, 'S S S S S H H Su Su Su')
        hand = makeSoft(4)
        self.assertRow(chart, hand, 'S S S S S H H H Su H')
        hand = makeSoft(3)
        self.assertRow(chart, hand, 'S S S S S H H H H H')
        hand = makeSoft(2)
        self.assertRow(chart, hand, 'S S S S S H H H H H')
        
        # test pair advice -- should be same
        hand = makePair('A')
        self.assertRow(chart, hand, 'H  H S S S H H H H H')
        hand = makePair(10)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makePair(9)
        self.assertRow(chart, hand, 'S S S S S S S S S S')
        hand = makePair(8)
        self.assertRow(chart, hand, 'S S S S S H H Su Su Su')
        hand = makePair(7)
        self.assertRow(chart, hand, 'S S S S S H H H H H')
        hand = makePair(6)
        self.assertRow(chart, hand, 'H H S S S H H H H H')
        hand = makePair(5)
        self.assertRow(chart, hand, 'Dh Dh Dh Dh Dh Dh Dh Dh H H')
        hand = makePair(4)
        self.assertRow(chart, hand, 'H H H H H H H H H H')
        hand = makePair(3)
        self.assertRow(chart, hand, 'H H H H H H H H H H')
        hand = makePair(2)
        self.assertRow(chart, hand, 'H H H H H H H H H H')

def makePair(rank):
    hand = BlackjackHand()
    hand.addCards(Card(rank, 'H'), Card(rank, 'C'))
    return hand

def makeSoft(rank):
    hand = BlackjackHand()
    hand.addCards(Card('A', 'H'), Card(rank, 'D'))
    return hand

def makeHand(r1, r2):
    hand = BlackjackHand()
    hand.addCards(Card(r1, 'H'), Card(r2, 'S'))
    return hand
        
if __name__ == '__main__':
    unittest.main()

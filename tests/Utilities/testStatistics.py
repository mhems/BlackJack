import unittest
from src.Utilities.Statistics import *

class testStatistics(unittest.TestCase):
    def setUp(self):
        self.empty  = []
        self.array1 = [1]
        self.array2 = [3, -4]
        self.array3 = [3, 2, -1, 6, -3, 0, 2, 0, 5]
        self.array4 = [-1, 3, -2, 1, 1, 4, -5]
        self.array5 = [1, 0, -1, 0, 0, 1, 1, -1, 2, -1]
        self.array6 = [40, 20, 1, -10, -15, 0, 30, -31, 23]
        self.array7 = [10, 10, 10, 10, 10, 10]

    def tearDown(self):
        pass

    def testmean(self):
        self.assertIs(mean(self.empty),  None)
        self.assertAlmostEqual(mean(self.array1), 1.0)
        self.assertAlmostEqual(mean(self.array2), -0.5)
        self.assertAlmostEqual(mean(self.array3), 1.5555555555)
        self.assertAlmostEqual(mean(self.array4), 0.142857142857)
        self.assertAlmostEqual(mean(self.array5), 0.2)
        self.assertAlmostEqual(mean(self.array6), 6.4444444444)
        self.assertAlmostEqual(mean(self.array7), 10.0)

    def testmedian(self):
        self.assertIs(median(self.empty),  None)
        self.assertAlmostEqual(median(self.array1), 1.0)
        self.assertAlmostEqual(median(self.array2), -0.5)
        self.assertAlmostEqual(median(self.array3), 2.0)
        self.assertAlmostEqual(median(self.array4), 1.0)
        self.assertAlmostEqual(median(self.array5), 0.0)
        self.assertAlmostEqual(median(self.array6), 1.0)
        self.assertAlmostEqual(median(self.array7), 10.0)

    def testmode(self):
        self.assertIs(mode(self.empty),  None)
        self.assertEqual(mode(self.array1), 1)
        self.assertCountEqual(mode(self.array2), [3, -4])
        self.assertCountEqual(mode(self.array3), [2, 0])
        self.assertEqual(mode(self.array4), 1)
        self.assertCountEqual(mode(self.array5), [1, 0, -1])
        self.assertCountEqual(mode(self.array6), [40, 20, 1, -10, -15, 0, 30, -31, 23])
        self.assertEqual(mode(self.array7), 10)

    def testfrequency_dict(self):
        self.assertEqual(frequency_dict(self.empty),  {})
        self.assertEqual(frequency_dict(self.array1),
                         {1:1})
        self.assertEqual(frequency_dict(self.array2),
                         {3:1, -4:1})
        self.assertEqual(frequency_dict(self.array3),
                         {3:1, 2:2, -1:1, 6:1, -3:1, 0:2, 5:1})
        self.assertEqual(frequency_dict(self.array4),
                         {-1:1, 3:1 ,-2:1, 1:2, 4:1, -5:1})
        self.assertEqual(frequency_dict(self.array5),
                         {1:3, 0:3, -1:3, 2:1})
        self.assertEqual(frequency_dict(self.array6),
                         {40:1, 20:1, 1:1, -10:1, -15:1,
                          0:1, 30:1, -31:1, 23:1})
        self.assertEqual(frequency_dict(self.array7),
                         {10:6})

    def testvariance(self):
        self.assertIs(variance(self.empty),  None)
        self.assertAlmostEqual(variance(self.array1), 0.0)
        self.assertAlmostEqual(variance(self.array2), 12.25)
        self.assertAlmostEqual(variance(self.array3), 7.35802469136)
        self.assertAlmostEqual(variance(self.array4), 8.12244897959)
        self.assertAlmostEqual(variance(self.array5), 0.96)
        self.assertAlmostEqual(variance(self.array6), 482.469135802)
        self.assertAlmostEqual(variance(self.array7), 0.0)

    def teststddev(self):
        self.assertIs(stddev(self.empty),  None)
        self.assertAlmostEqual(stddev(self.array1), 0.0)
        self.assertAlmostEqual(stddev(self.array2), 3.5)
        self.assertAlmostEqual(stddev(self.array3), 2.71256791461)
        self.assertAlmostEqual(stddev(self.array4), 2.84999104904)
        self.assertAlmostEqual(stddev(self.array5), 0.979795897113)
        self.assertAlmostEqual(stddev(self.array6), 21.9651800767)
        self.assertAlmostEqual(stddev(self.array7), 0.0)

    def testdelta(self):
        self.assertIs(delta(self.empty),  None)
        self.assertEqual(delta(self.array1), 0)
        self.assertEqual(delta(self.array2), 7)
        self.assertEqual(delta(self.array3), 9)
        self.assertEqual(delta(self.array4), 9)
        self.assertEqual(delta(self.array5), 3)
        self.assertEqual(delta(self.array6), 71)
        self.assertEqual(delta(self.array7), 0)

    def testlength_longest_non_decreasing_run(self):
        self.assertIs(length_longest_non_decreasing_run(self.empty),  None)
        self.assertEqual(length_longest_non_decreasing_run(self.array1), 1)
        self.assertEqual(length_longest_non_decreasing_run(self.array2), 1)
        self.assertEqual(length_longest_non_decreasing_run(self.array3), 3)
        self.assertEqual(length_longest_non_decreasing_run(self.array4), 4)
        self.assertEqual(length_longest_non_decreasing_run(self.array5), 5)
        self.assertEqual(length_longest_non_decreasing_run(self.array6), 3)
        self.assertEqual(length_longest_non_decreasing_run(self.array7), 6)

    def testlength_longest_increasing_run(self):
        self.assertIs(length_longest_increasing_run(self.empty),  None)
        self.assertEqual(length_longest_increasing_run(self.array1), 1)
        self.assertEqual(length_longest_increasing_run(self.array2), 1)
        self.assertEqual(length_longest_increasing_run(self.array3), 3)
        self.assertEqual(length_longest_increasing_run(self.array4), 2)
        self.assertEqual(length_longest_increasing_run(self.array5), 2)
        self.assertEqual(length_longest_increasing_run(self.array6), 3)
        self.assertEqual(length_longest_increasing_run(self.array7), 1)

    def testlength_longest_non_increasing_run(self):
        self.assertIs(length_longest_non_increasing_run(self.empty),  None)
        self.assertEqual(length_longest_non_increasing_run(self.array1), 1)
        self.assertEqual(length_longest_non_increasing_run(self.array2), 2)
        self.assertEqual(length_longest_non_increasing_run(self.array3), 3)
        self.assertEqual(length_longest_non_increasing_run(self.array4), 2)
        self.assertEqual(length_longest_non_increasing_run(self.array5), 3)
        self.assertEqual(length_longest_non_increasing_run(self.array6), 5)
        self.assertEqual(length_longest_non_increasing_run(self.array7), 6)

    def testlength_longest_decreasing_run(self):
        self.assertIs(length_longest_decreasing_run(self.empty),  None)
        self.assertEqual(length_longest_decreasing_run(self.array1), 1)
        self.assertEqual(length_longest_decreasing_run(self.array2), 2)
        self.assertEqual(length_longest_decreasing_run(self.array3), 3)
        self.assertEqual(length_longest_decreasing_run(self.array4), 2)
        self.assertEqual(length_longest_decreasing_run(self.array5), 3)
        self.assertEqual(length_longest_decreasing_run(self.array6), 5)
        self.assertEqual(length_longest_decreasing_run(self.array7), 1)

    def testmaximum_subarray(self):
        self.assertEqual(maximum_subarray(self.empty),  (None,0))
        self.assertEqual(maximum_subarray(self.array1), (1,1))
        self.assertEqual(maximum_subarray(self.array2), (3,1))
        self.assertEqual(maximum_subarray(self.array3), (14,9))
        self.assertEqual(maximum_subarray(self.array4), (7,5))
        self.assertEqual(maximum_subarray(self.array5), (3,9))
        self.assertEqual(maximum_subarray(self.array6), (66,7))
        self.assertEqual(maximum_subarray(self.array7), (60,6))

if __name__ == '__main__':
    unittest.main()

from math import sqrt
from operator import (le, lt, ge, gt)

"""Functions to gather statistics on various data structures"""

# BASIC STATISTICS

def mean(sequence):
    """Computes the mean of the sequence"""
    n = len(sequence)
    if n == 0:
        return None
    return sum(sequence)/n

def median(sequence):
    """Computes the median of the sequence"""
    n = len(sequence)
    if n == 0:
        return None
    mid = n//2
    sseq = sorted(sequence)
    if n % 2 == 1:
        return sseq[mid]
    return (sseq[mid-1] + sseq[mid])/2

def mode(sequence):
    """Computes the mode of the sequence"""
    if len(sequence) == 0:
        return None
    fd = frequency_dict(sequence)
    m = max(fd.values())
    mode = [key for (key, val) in fd.items() if val == m]
    if len(mode) == 1:
        return mode[0]
    return mode

def frequency_dict(sequence):
    """Computes the frequency of each element in sequence"""
    d = {}
    for e in sequence:
        if e in d:
            d[e] += 1
        else:
            d[e]  = 1
    return d

def variance(sequence):
    """Computes the variance of the sequence"""
    n = len(sequence)
    if n == 0:
        return None
    return sum(map(lambda x: x * x, sequence))/n - (mean(sequence) ** 2)

def stddev(sequence):
    """Computes the standard deviation of the sequence"""
    if len(sequence) == 0:
        return None
    return sqrt(variance(sequence))

def delta(sequence):
    """Computes difference between max and min of sequence"""
    if len(sequence) == 0:
        return None
    return max(sequence) - min(sequence)

# RUN STATISTICS

def length_longest_non_decreasing_run(sequence):
    """Computes the length of the longest non-decreasing run"""
    return length_longest_run(sequence, le)

def length_longest_increasing_run(sequence):
    """Computes the length of the longest increasing run"""
    return length_longest_run(sequence, lt)

def length_longest_non_increasing_run(sequence):
    """Computes the length of the longest non-increasing run"""
    return length_longest_run(sequence, ge)

def length_longest_decreasing_run(sequence):
    """Computes the length of the longest decreasing run"""
    return length_longest_run(sequence, gt)

def length_longest_run(sequence, predicate):
    """Computes the length of the longest run in sequence
       such that each pair of adjacent items satisfies binary predicate"""
    n = len(sequence)
    if n == 0:
        return None
    best = 1
    for start in range(0, n-1):
        index = start
        while index < n - 1 and predicate(sequence[index], sequence[index+1]):
            index += 1
        res = index - start + 1
        if res > best:
            best = res
    return best


def maximum_subarray(sequence):
    """Computes the maximum subarray of sequence,
       Returns (maximum sum, length of maximum subarray"""
    # Kadane's algorithm adapted from wikipedia
    if len(sequence) == 0:
        return (None, 0)
    local_max = global_max = sequence[0]
    local_count = global_count = 1
    for item in sequence[1:]:
        if item > local_max + item:
            local_max = item
            local_count = 1
        else:
            local_max += item
            local_count += 1
        if local_max > global_max:
            global_max = local_max
            global_count = local_count
    return (global_max, global_count)

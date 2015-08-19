####################
#
# Statistics.py
#
####################

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
    pass

def mode(sequence):
    """Computes the mode of the sequence"""
    pass

def frequency_dict(sequence):
    """Computes the frequency of each element in sequence"""
    pass

def variance(sequence):
    """Computes the variance of the sequence"""
    pass

def stddev(sequence):
    """Computes the standard deviation of the sequence"""
    pass

def delta(sequence):
    """Computes difference between max and min of sequence"""
    pass

# RUN STATISTICS

def length_longest_non_decreasing_run(sequence):
    """Computes the length of the longest non-decreasing run"""
    pass

def length_longest_increasing_run(sequence):
    """Computes the length of the longest increasing run"""
    pass

def length_longest_non_increasing_run(sequence):
    """Computes the length of the longest non-increasing run"""

def length_longest_decreasing_run(sequence):
    """Computes the length of the longest decreasing run"""
    pass

def maximum_subarray(sequence):
    """Computes the maximum subarray of sequence"""
    pass

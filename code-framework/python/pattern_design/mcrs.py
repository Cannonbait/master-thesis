from pattern_design.pattern_interface import IPatternGenerator
import numpy as np
import math
import random
# Chinese reaminder sieve
# This construction is deterministic, hence many pattern trials
# are not neccessary. The patterns could then be generated in a constructor
# and used for any number of items.
class MCRS(IPatternGenerator):

    def generate_patterns(m,n,d,b):
        # These primes are taken straight from the EGH-filter paper
        # (Usage: m = 501, n = 6996 to replicate their results)
        # For real applications, these should be computed using some sieve.
        # (perhaps already in constructor)
        #
        k = int(round(b*m/d*math.log(2)))
        k = max(k, 1)
        # Hardcoded for testing
        if k == 1:
            primes = [509]
        elif k == 2:
            primes = [241,269]
        elif k == 3:
            primes = [151,179,181]
        elif k == 4:
            primes = [127,131,137,113]
        elif k == 5:
            primes = [101,103,107,73,127]
        elif k == 6:
            primes = [61, 79, 83, 89, 97, 101]
        elif k == 7: #d >= 50
            primes = [83, 59, 61, 67, 71, 73, 97]
        else:
            primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]

        #primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]
        patterns = np.zeros((m,n))
        for i in range(n):
            current_index = 0
            for p in primes:
                index = (i % p) + current_index
                patterns[index][i] = 1
                current_index += p
        return patterns

    def get_name():
        return "MCRS"

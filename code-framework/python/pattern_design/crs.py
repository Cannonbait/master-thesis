from pattern_design.pattern_interface import IPatternGenerator
import numpy as np
import math
import random
# Chinese reaminder sieve
# This construction is deterministic, hence many pattern trials
# are not neccessary. The patterns could then be generated in a constructor
# and used for any number of items.
class CRS(IPatternGenerator):

    def generate_patterns(m,n,d,b):
        # These primes are taken straight from the EGH-filter paper
        # (Usage: m = 501, n = 6996 to replicate their results)
        # For real applications, these should be computed using some sieve.
        # (perhaps already in constructor)
        #
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]
        patterns = np.zeros((m,n))
        for i in range(n):
            current_index = 0
            for p in primes:
                index = (i % p) + current_index
                patterns[index][i] = 1
                current_index += p
        return patterns

    def get_name():
        return "CRS"

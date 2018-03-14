from pattern_interface import IPatternGenerator
import numpy as np
import math
import random

class COMP(IPatternGenerator):

    def generate_patterns(m,n,d,b):
        patterns = np.zeros((n,m), dtype='bool')
        for i in range(m):
            for j in range(n):
                r = random.random()
                if r <= b/d:
                    patterns[j][i] = 1
        return patterns

    def get_name():
        return "COMP"

# Cache- Hash-efficient
class CHE(IPatternGenerator):

    def generate_patterns(m,n,d,b):
        k = int(round(b*m/d*math.log(2)))
        k = max(k, 1)
        patterns = np.zeros((n,m))
        for j in range(n):
            for i in range(k):
                patterns[j][i] = 1
            random.shuffle(patterns[j])
        return patterns

    def get_name():
        return "CHE"

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
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]
        patterns = np.zeros((n,m))
        current_index = 0
        for p in primes:
            for x in range(p):
                hw = 0
                for i in range(n):
                    if(x == (i % p)):
                        patterns[i][current_index] = 1
                current_index += 1
        return patterns

    def get_name():
        return "CRS"

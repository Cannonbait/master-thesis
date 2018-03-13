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

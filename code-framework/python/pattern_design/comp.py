from pattern_design.pattern_interface import IPatternGenerator
import numpy as np
import math
import random

class COMP(IPatternGenerator):

    def generate_patterns(m,n,d,b):
        patterns = np.zeros((m,n), dtype='bool')
        for i in range(m):
            for j in range(n):
                r = random.random()
                if r <= b/d:
                    patterns[i][j] = 1
        return patterns

    def get_name():
        return "COMP"

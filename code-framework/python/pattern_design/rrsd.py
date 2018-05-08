from pattern_design.pattern_interface import IPatternGenerator
import numpy as np
import math
import random
# Cache- Hash-efficient
class RrSD(IPatternGenerator):

    def generate_patterns(m,n,d,b):
        r = int(round(b*n*math.log(2)/(d)))
        patterns = np.zeros((m,n))
        for i in range(m):
            for j in range(r):
                patterns[i][j] = 1
            random.shuffle(patterns[i,:])
        return patterns

    def get_name():
        return "RrSD"

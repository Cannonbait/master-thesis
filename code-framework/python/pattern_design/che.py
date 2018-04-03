from pattern_design.pattern_interface import IPatternGenerator
import numpy as np
import math
import random
# Cache- Hash-efficient
class CHE(IPatternGenerator):

    def generate_patterns(m,n,d,b):
        k = int(round(b*m/d*math.log(2)))
        k = max(k, 1)
        patterns = np.zeros((m,n))
        for i in range(n):
            for j in range(k):
                patterns[j][i] = 1
            random.shuffle(patterns[:,i])
        return patterns

    def get_name():
        return "CHE"

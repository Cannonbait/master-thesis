from pattern_interface import IPattern
from numpy import matrix, zeros
from random import random

class COMP(IPattern):
    patterns = None

    def __init__(self,m,n,d):
        self.patterns = zeros((m,n))
        for i in range(m):
            for j in range(n):
                r = random()
                if r <= 1/d:
                    self.patterns[i][j] = 1

    def patterns(self):
        return self.patterns

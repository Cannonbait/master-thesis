import numpy as np
import random
import math

#--------------------------------------------#
#   When adding new pattern designs, please  #
#   note that the FilterFramework accepts    #
#   numpy matrixes as input. Hence these     #
#   functions should return a matrix.        #
#--------------------------------------------#

# COMP patter design
def comp(m,n,d,b):
    patterns = np.zeros((n,m))
    for i in range(m):
        for j in range(n):
            r = random()
            if r <= b/d:
                patterns[j][i] = 1
    return patterns

# Pattern design from Cache- Hash-efficient Bloom filters
def che(m,n,d,b):
    k = int(round(b*m/d*math.log(2)))
    patterns = np.zeros((n,m))
    for j in range(n):
        for i in range(k):
            patterns[j][i] = 1
        random.shuffle(patterns[j])
    return patterns

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
            r = random.random()
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

def neigh(m,n,d,b):
    k = int(round(b*m/d*math.log(2)))
    patterns = np.zeros((n,m))
    for j in range(n):
        for i in range(k+1):
            patterns[j][i] = 1
        random.shuffle(patterns[j])
    return patterns

def ident(m,n):
    patterns = np.zeros((n,m))
    for j in range(n):
        patterns[j][j] = 1
    return patterns

# Probabilistic q-ary design
# Note: Las Vegas algorithm, failure rate 50%
def pqd(m,n,d,b):
    eta = 3.92
    q = (1+eta)*d
    p = 0.9
    t_0 = round(math.log((2*n-1)/(1-p))*d*(1+eta)/eta)
    n_0 = 2*n
    # Construct a random q-ary matrix
    qary = np.zeros((n,m))
    for i in range(n):
        for j in range(m):
            quary[i][j] = randomint(0,round(q-1))

    #for j in range():
    return quary

import numpy as np
import random
import math
import sys
from sklearn.cluster import KMeans
import scipy.spatial

#--------------------------------------------#
#   When adding new pattern designs, please  #
#   note that the FilterFramework accepts    #
#   numpy matrixes as input. Hence these     #
#   functions should return a matrix.        #
#--------------------------------------------#

def hamdist(vec1, vec2):
   return np.sum(np.logical_xor(vec1, vec2))

def better(m,n,d,b):
    k = int(round(b*m/d*math.log(2)))
    k = max(k, 1)
    nmbr_of_redoes = 0
    patterns = np.zeros((n,m))
    for j in range(n):
        not_unique = True
        while(not_unique):
            pattern = np.zeros(m)
            for i in range(k):
                pattern[i] = 1
            random.shuffle(pattern)
            print(j)
            # Check for overlap
            not_unique = False
            if(j > 0):
                for v in range(j):
                    other = patterns[v]
                    if(hamdist(pattern,other) < k):
                        not_unique = True
                        nmbr_of_redoes = nmbr_of_redoes + 1
                        break
        patterns[j] = pattern
    print("Done, redoes where: ", nmbr_of_redoes)
    return patterns

def eta_estimate(m,n,k,h,H):
    denom = 2.72**(3*(k-m*(k-H/2))/((h+H)*(2*m*(k-H/2) + k)))
    return n/denom

def pattern_hamdist(patterns):
    (n,m) = patterns.shape
    min_dist = m
    a = np.zeros(n)
    for i in range(1,n):
        b = np.zeros(i)
        for j in range(i):
            dist = hamdist(patterns[i],patterns[j])
            if min_dist > dist:
                min_dist = dist
            b[j] = dist
        a[i] = np.mean(b)
    return (min_dist,np.mean(a))

# Randomizes 20 pattern designs
# and takes the best one according
# to Mazumdar's theorem
def multiple_cher(m,n,d,b):
    designs = 20
    est_eta = [None]*designs
    k = int(round(b*m/d*math.log(2)))
    k = max(k, 1)
    for design in range(designs):
        patterns = che(m,n,d,b)
        (h,H) = pattern_hamdist(patterns)
        #est_eta[design] = eta_estimate(m,n,k,h,H)
        est_eta[design] = H-h
    print("estimated ETA: ", est_eta)

# COMP patter design
def comp(m,n,d,b):
    patterns = np.zeros((n,m), dtype='bool')
    for i in range(m):
        for j in range(n):
            r = random.random()
            if r <= b/d:
                patterns[j][i] = 1
    return patterns

# COMP++ patter design
def comp2(m,n,d,b):
    patterns = np.zeros((n,m))
    for i in range(m):
        for j in range(n):
            r = random.random()
            if r <= b*math.log(2)/d:
                patterns[j][i] = 1
    return patterns

# DOES NOT WORK
def cluster(m,n,d,b):
    k = int(round(b*m/d*math.log(2)))
    k = max(k, 1)
    patterns = np.zeros((n*10,m))
    kmeans = KMeans(n_clusters=n, random_state=0).fit(patterns)
    kmeans.labels_
    for j in range(n*10):
        for i in range(k):
            patterns[j][i] = 1
        random.shuffle(patterns[j])
    print(patterns)
    return kmeans.cluster_centers_

# Pattern design from Cache- Hash-efficient Bloom filters
def che(m,n,d,b):
    k = int(round(b*m/d*math.log(2)))
    k = max(k, 1)
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

def divisorGenerator(n):
    for i in xrange(1,n/2+1):
        if n%i == 0: yield i
    yield n

# A somewhat modified rank-and-winnow protocol
# since our tests are limited, hence we adjust
# the value d to be the nearest divior of m/2.
def rankandwinnow(m,n,d,b):
    t = m//2
    k = t//d
    patterns = np.zeros((n,m))
    for j in range(n):
        for i in range(k):
            patterns[j][i] = 1
        random.shuffle(patterns[j])
    return patterns

# Probabilistic q-ary design
# Note: Las Vegas algorithm, failure rate 10%
def pqd(m,n,d,b):
    eta = 3.92
    z = 4 # Default value
    p = 0.1
    q = (1+eta)*d + eta*z/(math.log((2*n-1)/(1-p)))
    print("q: ",q)
    t_0 = round(math.log((2*n-1)/(1-p))*d*(1+eta)/eta)
    n_0 = 2*n
    my = t_0/q
    print("my: ", my)
    # Construct a random q-ary matrix
    qary = np.zeros((t_0,n_0))
    print(qary.shape)
    for i in range(t_0):
        for j in range(n_0):
            qary[i][j] = round(random.random()*(q)+1)

    for j in range(1,n_0):
        for i in range(j):
            print(i)
    return qary

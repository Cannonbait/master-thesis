from lcgfilter import PyLCGFilter
from crsfilter import PyCRSFilter
from pbloom import PyPatternBF
import matplotlib.pyplot as plt
import numpy as np
import math

def progbar(curr, total, full_progbar):
    frac = curr/total
    filled_progbar = round(frac*full_progbar)
    print('\r', '#'*filled_progbar + '-'*(full_progbar-filled_progbar), '[{:>7.2%}]'.format(frac), end='')


# CONSTANTS
D_START = 180
D_STEP  = 2
D_END   = 200
BITS    = 509
BLOCKS  = 1
TESTS   = 100000
LOOPS   = 30

x = range(D_START,D_END,D_STEP)

# RESULT VECTORS
lcg = [None]*len(x)
crs = [None]*len(x)
fil = [None]*len(x)
lcgloops = [None]*LOOPS
crsloops = [None]*LOOPS
filloops = [None]*LOOPS
lcgdev = [None]*len(x)
crsdev = [None]*len(x)
fildev = [None]*len(x)

total = LOOPS*len(x)


# MAIN LOOP
for ind, d in enumerate(x):
    for j in range(LOOPS):
        lcgfilt = PyLCGFilter(BITS,BLOCKS,d)
        crsfilt = PyCRSFilter(BITS,BLOCKS,d)
        filt    = PyPatternBF(1,d,BLOCKS,BITS)
        k = round(math.log(2)*BITS/d)
        # Populate filters
        for i in range(d):
            lcgfilt.add_random()
            crsfilt.add_random()
            filt.add_random(0.0,k)


        false_positives_lcg = 0
        false_positives_crs = 0
        false_positives_fil = 0
        for i in range(TESTS):
            if(lcgfilt.try_random()):
                false_positives_lcg = false_positives_lcg + 1
            if(crsfilt.try_random()):
                false_positives_crs = false_positives_crs + 1
            if(filt.test_random_pattern(0.0,k)):
                false_positives_fil = false_positives_fil + 1
        lcgloops[j] = false_positives_lcg/TESTS
        crsloops[j] = false_positives_crs/TESTS
        filloops[j] = false_positives_fil/TESTS
    progbar(d-D_START+1,(D_END-D_START),40)
    lcg[ind] = np.mean(lcgloops)
    crs[ind] = np.mean(crsloops)
    fil[ind] = np.mean(filloops)
    lcgdev[ind] = np.std(lcgloops)
    crsdev[ind] = np.std(crsloops)
    fildev[ind] = np.std(filloops)

fig, ax = plt.subplots()
x = np.linspace(D_START,D_END,len(x))
ax.errorbar(x,lcg,lcgdev,fmt='-o')
ax.errorbar(x,crs,crsdev,fmt='-o')
ax.errorbar(x, fil,fildev,fmt='-o')
ax.grid(True)
plt.xlabel("d",fontsize=16)
plt.ylabel("FPR",fontsize=16)
plt.legend(["LCG-run-time pattern generator","MCRS-run-time pattern generator","Bloom filter"])
plt.title("False positive rate as a funtion of d",fontsize=16)
plt.show()

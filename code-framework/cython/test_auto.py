from lcgfilter import PyLCGFilter
from crsfilter import PyCRSFilter
import matplotlib.pyplot as plt
import numpy as np
import math

def progbar(curr, total, full_progbar):
    frac = curr/total
    filled_progbar = round(frac*full_progbar)
    print('\r', '#'*filled_progbar + '-'*(full_progbar-filled_progbar), '[{:>7.2%}]'.format(frac), end='')


# CONSTANTS
D_START = 50
D_END   = 200
BITS    = 512
BLOCKS  = 1
TESTS   = 100000
LOOPS   = 40

# RESULT VECTORS
lcg = [None]*(D_END-D_START)
crs = [None]*(D_END-D_START)
lcgloops = [None]*LOOPS
crsloops = [None]*LOOPS

total = LOOPS*(D_END-D_START)
x = range(D_START,D_END)

# MAIN LOOP
for d in x:
    for j in range(LOOPS):
        lcgfilt = PyLCGFilter(BITS,BLOCKS,d)
        crsfilt = PyCRSFilter(BITS,BLOCKS,d)
        # Populate filters
        for i in range(d):
            lcgfilt.add_random()
            crsfilt.add_random()

        false_positives_lcg = 0
        false_positives_crs = 0
        for i in range(TESTS):
            if(lcgfilt.try_random()):
                false_positives_lcg = false_positives_lcg + 1
            if(crsfilt.try_random()):
                false_positives_crs = false_positives_crs + 1
        lcgloops[j] = false_positives_lcg/TESTS
        crsloops[j] = false_positives_crs/TESTS
    progbar(d-D_START+1,(D_END-D_START),40)
    lcg[d-D_START] = np.mean(lcgloops)
    crs[d-D_START] = np.mean(crsloops)

fig, ax = plt.subplots()
x = np.linspace(D_START,D_END,(D_END-D_START))
ax.plot(x,lcg)
ax.plot(x,crs)
ax.plot(x, (1-math.e**(-(math.log(2)*BLOCKS*BITS/x)*x/BITS*BLOCKS))**(math.log(2)*BLOCKS*BITS/x))
plt.xlabel("Stored items")
plt.ylabel("FPR")
plt.legend(["LCG-generator","CRS-generator","Theoretical Bloom filter"])
plt.title("False positive rate as a funtion of stored items")
plt.show()

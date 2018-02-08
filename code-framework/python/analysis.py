import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('../cython/')
import framework

NUM_PATTERNS_START = 5
NUM_PATTERNS_END = 30
ITEMS_TO_STORE = 30
NUM_BLOCKS = 30
NUM_BITS = 500
NUM_TESTS = 10000


testResults = []

for i in range(NUM_PATTERNS_START, NUM_PATTERNS_END):
    p = framework.PyFilterFramework(i, ITEMS_TO_STORE, NUM_BLOCKS, NUM_BITS)
    for i in range(0, ITEMS_TO_STORE):
        p.add_item()
    testResult = p.test_framework(NUM_TESTS)
    testResults.append(testResult)
    
    
ts = pd.Series(testResults, range(NUM_PATTERNS_START, NUM_PATTERNS_END))
plt.figure()
ts.plot()
plt.show()

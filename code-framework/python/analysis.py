import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('../cython/')
import framework
import sys
sys.argv[1:] = ["--source=../data-preparation/babesia-bovis/babesia_bovis.prep"]
from mpl_toolkits.mplot3d import Axes3D
np.set_printoptions(formatter={'float': '{: 0.3f}'.format})

NUM_PATTERNS = 20
NUM_PATTERNS_START = 20
NUM_PATTERNS_END = 30
ITEMS_TO_STORE_START = 1
ITEMS_TO_STORE_END = 50
NUM_BLOCKS = 30
NUM_BITS = 15
NUM_TESTS = 1000

if any([s.startswith("--source=") for s in sys.argv]):
    fileName = [x for x in sys.argv if x.startswith("--source=")][0][9:]
    p = framework.PyFilterFramework(NUM_PATTERNS, 17, 20, NUM_BITS)
    p.add_items_from_path(5, fileName)
    print(p.test_framework(5))
    
##
##x = np.arange(NUM_PATTERNS_START, NUM_PATTERNS_END)
##y = np.arange(ITEMS_TO_STORE_START, ITEMS_TO_STORE_END)
##z = np.zeros([y.size, x.size])
##
##
##for ix, num_patterns in enumerate(x):
##    values = []
##    for iy, num_to_store in enumerate(y):
##        p = framework.PyFilterFramework(num_patterns, num_to_store, NUM_BLOCKS, NUM_BITS)
##        for i in range(0, num_to_store):
##            p.add_items(5)
##        testResult = p.test_framework(NUM_TESTS)
##        z[iy][ix] = testResult
##
##fig = plt.figure()
##ax = fig.gca(projection='3d')
##x, y = np.meshgrid(x, y)
##ax.plot_surface(x,y,z)
##plt.show()

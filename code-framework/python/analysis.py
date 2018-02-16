import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('../cython/')
import framework
import sys
sys.argv[1:] = ["--source=../data-preparation/babesia-bovis/babesia_bovis_pt1.prep"]
from mpl_toolkits.mplot3d import Axes3D
np.set_printoptions(formatter={'float': '{: 0.3f}'.format})

NUM_PATTERNS = 30; ## BE CAREFUL CHANGING THIS, SHOULD BE 30
NUM_TO_STORE = 1;
NUM_BLOCKS = 30; ## BE CAREFUL CHANGING THIS, SHOULD BE 30
NUM_BITS = 1;
NUM_TESTS = 50000;


## bits, patterns, item, blocks

if any([s.startswith("--source=") for s in sys.argv]):
    fileName = [x for x in sys.argv if x.startswith("--source=")][0][9:]
    p1 = framework.PyFilterFramework(NUM_BITS, NUM_PATTERNS, NUM_TO_STORE, NUM_BLOCKS)
    p1.add_items(NUM_TO_STORE)
    print(p1.test_framework(NUM_TESTS))
    p2 = framework.PyFilterFramework(NUM_BITS, NUM_PATTERNS, NUM_TO_STORE, NUM_BLOCKS)
    p2.add_items_from_path(NUM_TO_STORE, fileName)
    print(p2.test_framework_from_path(fileName))
    
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

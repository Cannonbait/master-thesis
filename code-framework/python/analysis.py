import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('../cython/')
import framework
import sys
import pattern_designs
## sys.argv[1:] = ["--source=../data-preparation/babesia-bovis/babesia_bovis_raw1.prep"]
from mpl_toolkits.mplot3d import Axes3D
from progress.bar import Bar
np.set_printoptions(formatter={'float': '{: 0.3f}'.format})

NUM_BITS = 512;
NUM_TESTS = 1000;
NUM_BLOCKS = 10
## bits, patterns, item, blocks


if any([s.startswith("--source=") for s in sys.argv]):
    NUM_PATTERNS = 30; ## BE CAREFUL CHANGING THIS, SHOULD BE 30
    NUM_TO_STORE = 40;
    NUM_BLOCKS = 30; ## BE CAREFUL CHANGING THIS, SHOULD BE 30
    p1 = framework.PyFilterFramework(NUM_BITS, NUM_PATTERNS, NUM_TO_STORE, NUM_BLOCKS)
    p1.add_items(NUM_TO_STORE)
    print(p1.test_framework(NUM_TESTS))
    p2 = framework.PyFilterFramework(NUM_BITS, NUM_PATTERNS, NUM_TO_STORE, NUM_BLOCKS)
    p2.add_items_from_path(NUM_TO_STORE, fileName)
    print(p2.test_framework_from_path(fileName))
    
else:
    NUM_PATTERNS_START = 650
    NUM_PATTERNS_END = 720
    NUM_STORED_START = 20
    NUM_STORED_END = 40
    NUM_BLOCKS = 10
    STEP_SIZE = 10
    PATTERN_TRIALS = 1
    
    x = np.arange(NUM_PATTERNS_START, NUM_PATTERNS_END, STEP_SIZE)
    y = np.arange(NUM_STORED_START, NUM_STORED_END, STEP_SIZE)
    comp = np.zeros([y.size, x.size])
    che = np.zeros([y.size, x.size])

    bar = Bar('Processing', max=x.size)
    for ix, num_patterns in enumerate(x):
        values = []
        for iy, num_to_store in enumerate(y):
            for trial in range(0, PATTERN_TRIALS):
                f = framework.PyFilterFramework(NUM_BITS, num_patterns, num_to_store, NUM_BLOCKS)
                f.replace_patterns(pattern_designs.comp(NUM_BITS, num_patterns, num_to_store, NUM_BLOCKS), num_to_store, NUM_BLOCKS)
                f.add_items(num_to_store)
                comp[iy][ix] = comp[iy][ix] + f.test_framework(NUM_TESTS)
                f.replace_patterns(pattern_designs.che(NUM_BITS, num_patterns, num_to_store, NUM_BLOCKS), num_to_store, NUM_BLOCKS)
                f.add_items(num_to_store)
                che[iy][ix] = che[iy][ix] + f.test_framework(NUM_TESTS)
            comp[iy][ix] = comp[iy][ix] / PATTERN_TRIALS
            che[iy][ix] = che[iy][ix] / PATTERN_TRIALS
        bar.next()
    bar.finish()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x, y = np.meshgrid(x, y)
    ax.plot_surface(x,y,comp)
    ax.plot_surface(x,y,che)
    plt.show()

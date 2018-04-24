# Blocked Bloom filter with bit-patterns framework
Master thesis at Chalmers 2018. A framework for testing Blocked Bloom filters with bit patterns (BBFBP) against real or simulated workloads. The framework allows users to send custom pattern designs to a BBFBP and compare its performance in terms of false positives to other designs.

The BBFBPs provided here are not written, or optimized, for commerical use. The filters lack support for SIMD-instructions which is neccessary for efficient filters of this type. 

# Installation
The analysis tools are bult in Python while the inner loop is written in C++. Bindings between these are provided by Cython and as such Python3 and the g++ compiler must be installed (atleast version 14), The instructions below assume that these exist on the users current machine. 

### Windows
```
Install boost from boost.org
```

### Ubuntu 16.04
```
$ apt-get install libboost-dev python3-numpy python3-tk libgmp3-dev
$ pip3 install cython matplotlib pandas
```

## Setup
After cloning the repository, move into the master-thesis/code-framework/ folder and execute 
the following commands. Given that all dependencies are installed as specified above, it will 
create a .so file which can be imported into python separately or used with the pre-built analysis program.

### Windows
```
$ cd <your path>/master-thesis/code-framework/cython
$ python3 setup_serial_framework_win.py
```

### Ubuntu 16.04
```
$ cd <your path>/master-thesis/code-framework/cython
$ python3 setup_serial_framework_nix.py build_ext --inplace
```
# Running the analysis tool
The analysis tool can be executed either from the command line for existing designs or through Python code with a few lines. Below are instructions on both of these cases.

## Command line 
From the command line the analysis tool can run for a number of parameters and existing designs. While this is not immediatly useful since you cannot pass new designs into the program this way, it helps the user get familiar with the parameters and how they can vary. 

To run a quick demo of the program, use the follwing commands which sould yield the following output:

```
$ cd <your path>/master-thesis/code-framework/python
$ python3 analysis.py -che -comp
Found no "source" argument, trials will be run with random input
Initializing filters...

```
This will run a quick demo comparing the CHE (Cache- Hash- efficent) and COMP (Combinatorial Orthogonal Matching Pursuit) algorithms as pattern designs for some default parameters. The execution time can vary from machine to machine depending on the cachesize. This should in the end display a graph looking something like this:

![Framework demo](https://github.com/Cannonbait/master-thesis/blob/master/readme_img.png)

Where the Y-axis represents the false positive rate (FPR) with standard deviation and the X-axis the number of insertions into the filter (d). These parameters can be customized be various flags supplied to the terminal. The customizable parameters are as follows:
```
-m=x                where x is the number of bits in the filter (defaults to 512)
-n=x                where x is the number of patterns in the filter (defaults to 4096)
-d=x                where x is the number of insertions in the filter (defaults to 120)
-b=x                where x is the number of blocks in the filter (defaults to 1)
-tests=x            where x is the number of tests on datapoints towards the filter. (defaults to 10000)
-step_size=x        where x is the step size on the varying parameter as explained below (defaults to 10)
-pattern_trials=x   where x is the number of times the patterns should be regenerated according to the specified designs and tested. This parameter affects the standard deviation in the graph (defaults to 5)
-comp               the COMP-algorithm as a pattern design (used for comparative purposes)
-che                the CHE-algorithm as a pattern design (used for comparative purposes)
-crs                the CRS-algorithm as a pattern design (used for comparative purposes)
-source="<file>"    a source file with precomputed data in number format, separated by linebreak. The framework allows for high precision and can parse numbers up to 120 characters long. These numbers are then hashed using modulohashing for a more uniform distribution. 
```
To be able to get a visualization, one or two parameters must vary. This is done by adding a new flag on the varying parameter(s) with "\_end" appended. For example, if one wants to experiment for varying values of d as in the example, one can choose the flags -d=120 and -d_end=160. The parameters that can vary are m, n, d and b. If two parameters vary, the displayed graph will be in three dimensions, for example:

```
$ python3 analysis.py -crs -comp -d=1200 -d_end=1600 -n=1500 -n_end=2000 -b=10 -step_size=100
Found no "source" argument, trials will be run with random input
Initializing filters...
```
## Python code

# Writing new patter-design generators
Writing a new generator is a fiarly easy task. Provided for guidance is an interface called __IPatternGenerator__ located in the *master-thesis/code-framework/python/pattern_design* folder. This interface is reuired of the generators to implement but only demands two definitions: *get_name* and *generate_patterns(m,n,d,b)*, where *generate_patterns* should return a matrix of dimensions *mxn* as patterns in the BBFBP. The *get_name* method is only used in the visualization for easy of identifying the new algorithm. Below is an example of a (stupid) pattern generator:

```python
from pattern_design.pattern_interface import IPatternGenerator
import numpy as np

class ExampleGenerator(IPatternGenerator):

    def generate_patterns(m,n,d,b):
        patterns = np.zeros((m,n), dtype='bool')
          for i in range(n):
            patterns[i % m][i] = 1
        return patterns

    def get_name():
        return "Example Generator"

```


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
$ apt-get install libboost-dev python3-numpy python3-tk
$ pip3 install cython matplotlib pandas
```

## Setup
After cloning the repository, move into the master-thesis/code-framework/ folder and execute 
the following commands. Given that all dependencies are installed as specified above, it will 
create a .so file which can be imported into python separately or used with the pre-built analysis program.

### Windows
```
$ cd cython
$ python3 setup_serial_framework_win.py
```

### Ubuntu 16.04
```
$ cd cython
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

Where the Y-axis represents the false positive rate (FPR) with standard deviation and the X-axis the number of insertions into the filter (d). These parameters can be customized be various flags supplied to the terminal.

## Python code

# Generating new pattern designs


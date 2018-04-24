# Blocked Bloom filter with bit-patterns framework
Master thesis at Chalmers 2018. A framework for testing Blocked Bloom filters with bit patterns (BBFBP) against real or simulated workloads. The framework allows users to send custom pattern designs to a BBFBP and compare its performance in terms of false positives to other designs.

The BBFBPs provided here are not written, or optimized, for commerical use. The filters lack support for SIMD-instructions which is neccessary for efficient filters of this type. 

# Installation
The analysis tools are bult in Python while the inner loop is written in C++. Bindings between these are provided by Cython and as such Python3, Cython and the g++ compiler must be installed (atleast version 14). The instructions below assume that these exist on the users current machine.

### Windows
Install boost from boost.org

### Ubuntu 16.04
On Ubuntu sudo apt-get install libboost-dev

## Setup
After cloning the repository, move into the master-thesis/code-framework/ folder and execute 
the following commands. Given that all dependencies are installed as specified above, it will 
create a .so file which can be imported into python separately or used with the pre-built analysis program.

### Windows
```
cd cython
python3 setup_serial_framework_win.py
```

### Ubuntu 16.04
```
cd cython
python3 setup_serial_framework_nix.py build_ext --inplace
```

## Ubuntu commands

```
apt-get install libboost-dev python3-pip python3 python3-numpy python3-tk
pip3 install cython matplotlib pandas
```

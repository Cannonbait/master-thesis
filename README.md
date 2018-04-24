# master-thesis
Master thesis at Chalmers 2018


# Installation
Install boost from boost.org
On Ubuntu sudo apt-get install libboost-dev

## Setup
After cloning the repository, move into the master-thesis/code-framework/ folder and execute 
the following commands. Given that all dependencies are installed as specified above, it will 
create a .so file which can be imported into python separately or used with the pre-built analysis program.

### Ubuntu 16.04
```
cd cython
python3 setup_serial_framework_nix.py build_ext --inplace

´´´

## Ubuntu commands

```
apt-get install libboost-dev python3-pip python3 python3-numpy python3-tk
pip3 install cython matplotlib pandas
´´´

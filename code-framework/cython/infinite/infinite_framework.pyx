# distutils: language = c++
# distutils: sources = ../core/infinite/infinite_framework.cpp

from infinite_framework cimport InfiniteFramework
from cpython.version cimport PY_MAJOR_VERSION
from libcpp.vector cimport vector
from libcpp cimport bool
from libcpp.string cimport string

cdef class PyInfiniteFramework:
    cdef InfiniteFramework infF
    def __cinit__(self):
      self.infF = InfiniteFramework()
    def test(self, store, blocks, tests, bits, level):
      return self.infF.test(store, blocks, tests, bits, level)

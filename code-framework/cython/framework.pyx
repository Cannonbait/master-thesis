# distutils: language = c++
# distutils: sources = ../core/filter_framework.cpp

from framework cimport FilterFramework
from cpython.version cimport PY_MAJOR_VERSION
from libcpp.vector cimport vector
from libcpp cimport bool

cdef class PyFilterFramework:
    cdef FilterFramework ff
    def __cinit__(self,int bits, int patterns, int items, int blocks):
      self.ff = FilterFramework(bits,patterns,items,blocks)
    def add_item(self,items):
      self.ff.add_items(items)
    def test_framework(self,tests):
      return self.ff.test_framework(tests)
    def replace_patterns(self,patterns,items,blocks):
      self.ff.replace_patterns(patterns,items,blocks)

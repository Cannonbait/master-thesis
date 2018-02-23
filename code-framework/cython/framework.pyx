# distutils: language = c++
# distutils: sources = ../core/filter_framework.cpp

from framework cimport FilterFramework
from cpython.version cimport PY_MAJOR_VERSION
from libcpp.vector cimport vector
from libcpp cimport bool
from libcpp.string cimport string

cdef class PyFilterFramework:
    cdef FilterFramework ff
    def __cinit__(self,int bits, int patterns, int items, int blocks):
      self.ff = FilterFramework(bits,patterns,items,blocks)
    def add_items(self,items):
      self.ff.add_items(items)
    def add_random(self,level_prob,k):
      self.ff.add_random(level_prob,k)
    def add_items_from_path(self,items, path):
      c_path = str.encode(path)
      self.ff.add_items_from_path(items, c_path)
    def test_framework(self,tests):
      return self.ff.test_framework(tests)
    def test_framework_from_path(self,path):
      c_path = str.encode(path)
      return self.ff.test_framework_from_path(c_path)
    def replace_patterns(self,patterns,items,blocks):
      self.ff.replace_patterns(patterns,items,blocks)
    def test_infinite_patterns(self,tests,level_prob):
      return self.ff.test_infinite_patterns(tests,level_prob)

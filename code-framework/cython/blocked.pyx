# distutils: language = c++
# distutils: sources = ../core/bloom_filter/blocked_filter.cpp

from blocked cimport BlockedFilter
from cpython.version cimport PY_MAJOR_VERSION
from libcpp cimport bool
from libcpp.string cimport string

cdef class PyBlockedFilter:
    cdef BlockedFilter bf
    def __cinit__(self,int bits, int blocks, int k, int seed):
      self.bf = BlockedFilter(bits,blocks,k,seed)
    def __cinit__(self,int bits, int blocks, int k):
      self.bf = BlockedFilter(bits,blocks,k)
    def add_item(self,s):
      c_string = str.encode(s)
      self.bf.add_item(c_string)
    def add(self):
      self.bf.add()
    def test_item(self,s):
      c_string = str.encode(s)
      return self.bf.test_item(c_string)
    def test(self):
      return self.bf.test()
    def display(self):
      self.bf.display()
    def hamming_weight(self):
      return self.bf.hamming_weight()

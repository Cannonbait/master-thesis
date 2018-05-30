# distutils: language = c++
# distutils: sources = ../core/patternbloom.cpp

from libcpp cimport bool
from pbloom cimport PatternBF
from libcpp.string cimport string
from cpython.version cimport PY_MAJOR_VERSION

cdef class PyPatternBF:
    cdef PatternBF c_pbf
    def __cinit__(self,int n, int d, int num_blocks, int num_bits):
      self.c_pbf = PatternBF(n,d,num_blocks, num_bits)
    def add(self,my_str):
      text = str.encode(my_str)
      self.c_pbf.add(text)
    def test(self,my_str):
      text = str.encode(my_str)
      return self.c_pbf.test(text)
    def add_many(self,int x):
      self.c_pbf.add_many(x)
    def test_rng(self):
      return self.c_pbf.test_rng()
    def test_random_pattern(self,level_prob,k):
      return self.c_pbf.test_random_pattern(level_prob,k)
    def add_random(self,level_prob,k):
      self.c_pbf.add_random(level_prob,k)

# distutils: language = c++
# distutils: sources = filter_framework.cpp

from framework cimport FilterFramework
from cpython.version cimport PY_MAJOR_VERSION

cdef class PyFilterFramework:
    cdef FilterFramework ff
    def __cinit__(self,int bits, int patterns, int items, int blocks):
      self.ff = FilterFramework(bits,patterns,items,blocks)
    def add_item(self):
      self.ff.add_item()
    def test_framework(self,tests):
      return self.ff.test_framework(tests)

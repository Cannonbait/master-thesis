# distutils: language = c++
# distutils: sources = ../core/runtime_filters/egh_filter.cpp

from eghfilter cimport EGHFilter

cdef class PyEGHFilter:
    cdef EGHFilter filt
    def __cinit__(self,int num_bits, int num_blocks, int items, int universe):
      self.filt = EGHFilter(num_bits,num_blocks,items,universe)
    def size(self):
      return self.filt.size()
    def try_random(self):
      return self.filt.try_random()
    def add_random(self):
      return self.filt.add_random()
    def measure_performance(self):
      return self.filt.measure_performance()

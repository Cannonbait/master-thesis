# distutils: language = c++
# distutils: sources = ../core/crs_filter/crs_filter.cpp

from crsfilter cimport CRSFilter

cdef class PyCRSFilter:
    cdef CRSFilter filt
    def __cinit__(self,int num_bits, int num_blocks, int items):
      self.filt = CRSFilter(num_bits,num_blocks,items)
    def size(self):
      return self.filt.size()
    def try_random(self):
      return self.filt.try_random()
    def add_random(self):
      return self.filt.add_random()

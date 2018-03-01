# distutils: language = c++
# distutils: sources = ../core/lcg_filter/lcg_filter.cpp

from lcgfilter cimport LCGFilter

cdef class PyLCGFilter:
    cdef LCGFilter filt
    def __cinit__(self,int num_bits, int num_blocks, int items):
      self.filt = LCGFilter(num_bits,num_blocks,items)
    def size(self):
      return self.filt.size()
    def try_random(self):
      return self.filt.try_random()
    def add_random(self):
      return self.filt.add_random()
    def change_lcg(self,new_mod,new_mul,new_inc):
      self.filt.change_lcg(new_mod,new_mul,new_inc)

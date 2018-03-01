cimport numpy as np
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "../core/lcg_filter/lcg_filter.h":
    cdef cppclass LCGFilter:
      LCGFilter() except +
      LCGFilter(int,int,int) except +
      unsigned int size()
      bool try_random()
      void add_random()
      void change_lcg(long,long,long)

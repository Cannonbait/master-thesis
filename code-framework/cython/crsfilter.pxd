cimport numpy as np
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "../core/crs_filter/crs_filter.h":
    cdef cppclass CRSFilter:
      CRSFilter() except +
      CRSFilter(int,int,int) except +
      unsigned int size()
      bool try_random()
      void add_random()

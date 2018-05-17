cimport numpy as np
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "../core/runtime_filters/egh_filter.h":
    cdef cppclass EGHFilter:
      EGHFilter() except +
      EGHFilter(int,int,int,int) except +
      unsigned int size()
      bool try_random()
      void add_random()
      double measure_performance()

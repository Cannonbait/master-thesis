cimport numpy as np
from libcpp cimport bool
from libcpp.vector cimport vector

cdef extern from "../core/filter_framework.h":
    cdef cppclass FilterFramework:
      FilterFramework() except +
      FilterFramework(int, int, int, int) except +
      void add_item()
      double test_framework(int)
      void replace_patterns(vector[vector[bool]], int, int)

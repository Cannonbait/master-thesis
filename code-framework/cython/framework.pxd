cimport numpy as np
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "../core/filter_framework.h":
    cdef cppclass FilterFramework:
      FilterFramework() except +
      FilterFramework(int, int, int, int) except +
      void add_items(int)
      void add_items_from_path(int, string)
      double test_framework(int)
      void replace_patterns(vector[vector[bool]], int, int)

cimport numpy as np
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "../core/bloom_filter/blocked_filter.h":
    cdef cppclass BlockedFilter:
      BlockedFilter() except +
      BlockedFilter(int, int, int) except +
      BlockedFilter(int, int, int, int) except +
      void add_item(string)
      bool test_item(string)
      void add()
      bool test()
      void display()

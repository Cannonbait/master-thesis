from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "../../core/infinite/infinite_framework.h":
    cdef cppclass InfiniteFramework:
      InfiniteFramework() except +
      double test(int, int, int, int, double)

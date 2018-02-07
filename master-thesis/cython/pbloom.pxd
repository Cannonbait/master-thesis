from libcpp cimport bool
from libcpp.string cimport string

cdef extern from "patternbloom.h":
    cdef cppclass PatternBF:
      PatternBF() except +
      PatternBF(int, int, int) except +
      void add(string)
      bool test(string)
      void add_many(int)
      bool test_rng()

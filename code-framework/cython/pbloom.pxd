from libcpp cimport bool
from libcpp.string cimport string

cdef extern from "../core/patternbloom.h":
    cdef cppclass PatternBF:
      PatternBF() except +
      PatternBF(int, int, int, int) except +
      void add(string)
      bool test(string)
      void add_many(int)
      bool test_rng()
      bool test_random_pattern(double,int)
      void add_random(double,int)

cdef extern from "../core/filter_framework.h":
    cdef cppclass FilterFramework:
      FilterFramework() except +
      FilterFramework(int, int, int, int) except +
      void add_item()
      double test_framework(int)

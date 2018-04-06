cimport numpy as np
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "../core/serial_framework.h":
    cdef cppclass SerialFramework:
      SerialFramework() except +
      SerialFramework(string) except +
      double test(vector[vector[bool]], int, int, int, int)
      double test_no_path(vector[vector[bool]], int, int, int, int)

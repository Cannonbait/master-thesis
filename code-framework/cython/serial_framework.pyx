# distutils: language = c++
# distutils: sources = ../core/serial_framework.cpp

from serial_framework cimport SerialFramework
from cpython.version cimport PY_MAJOR_VERSION
from libcpp.vector cimport vector
from libcpp cimport bool
from libcpp.string cimport string

cdef class PySerialFramework:
    cdef SerialFramework sf
    def __cinit__(self):
      self.sf = SerialFramework()
    def with_path(self, path):
      c_path = str.encode(path)
      self.sf = SerialFramework(c_path)
    def test(self, patterns, bits, store, blocks, tests):
      return self.sf.test(patterns.transpose(), bits, store, blocks, tests)
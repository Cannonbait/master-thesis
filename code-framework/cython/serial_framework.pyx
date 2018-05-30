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
	def add_source(self, source):
		self.sf.add_source(str.encode(source))
	def test(self, patterns, bits, store, blocks, tests, source):
		return self.sf.test(patterns.transpose(), bits, store, blocks, tests, str.encode(source))
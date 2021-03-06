from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy

setup(ext_modules = cythonize(Extension(
           "serial_framework",                                # the extension name
           sources=["serial_framework.pyx", "../core/serial_framework.cpp","../core/patternbloom.cpp"], # the Cython source and
                                                  # additional C++ source files
           language="c++",                        # generate and compile C++ code
           extra_compile_args=["/IC:/MinGW/include"],
           include_dirs=[numpy.get_include()]
      )))

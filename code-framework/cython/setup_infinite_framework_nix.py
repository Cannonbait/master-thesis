from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy

setup(ext_modules = cythonize(Extension(
           "infinite_framework",                                # the extension name
           sources=["infinite/infinite_framework.pyx", "../core/infinite/infinite_framework.cpp","../core/infinite/infinite_bloom.cpp"], # the Cython source and
                                                  # additional C++ source files
           language="c++",                       # generate and compile C++ code
           include_dirs = ['/usr/local/include'],
           libraries=['gmp','gmpxx','m'],
           library_dirs = ['/usr/local/lib'],
           extra_compile_args=["-std=c++14","-lgmp"],
      )))

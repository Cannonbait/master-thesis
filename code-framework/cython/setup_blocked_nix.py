from distutils.core import setup, Extension
from Cython.Build import cythonize

setup(ext_modules = cythonize(Extension(
           "blocked",                                # the extension name
           sources=["blocked.pyx", "../core/bloom_filter/blocked_filter.cpp","../core/bloom_filter/bloom_filter.cpp"], # the Cython source and
                                                  # additional C++ source files
           language="c++",                        # generate and compile C++ code
           extra_compile_args=["-std=c++14","-fPIC","-Wcpp","-O3"],
      )))

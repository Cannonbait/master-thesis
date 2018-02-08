from distutils.core import setup, Extension
from Cython.Build import cythonize

setup(ext_modules = cythonize(Extension(
           "framework",                                # the extension name
           sources=["framework.pyx", "filter_framework.cpp","worker.cpp","patternbloom.cpp"], # the Cython source and
                                                  # additional C++ source files
           language="c++",                        # generate and compile C++ code
           extra_compile_args=["-std=c++14","-lpthread","-fPIC"],
      )))

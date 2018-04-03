from distutils.core import setup, Extension
from Cython.Build import cythonize

setup(ext_modules = cythonize(Extension(
           "crsfilter",                                # the extension name
           sources=["crsfilter.pyx"], # the Cython source and
                                                  # additional C++ source files
           language="c++",                        # generate and compile C++ code
           extra_compile_args=["-std=c++14","-lpthread","-fPIC","-Wcpp","-O3"],
      )))

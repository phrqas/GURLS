import os
from setuptools import setup
from Cython.Build import cythonize

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="PyGURLS",
    version="0.0.1",
    author="Pedro Santana",
    author_email="psantana@mit.edu",
    description="A Python wrapper for the GURLS++/bGURLS++ libraries.",
    long_description=read("README"), #Reads from README in the same folder
    ext_modules = cythonize("pygurls.pyx",
                            sources=["../gurls++/src/gmath.cpp"],
                            language="c++")    
)

#setup(ext_modules = cythonize(
#            "pygurls.pyx", # our Cython source
#            sources=["../gurls++/src/options.cpp"],  # additional source file(s)
#            language="c++" # generate C++ code
#    ))
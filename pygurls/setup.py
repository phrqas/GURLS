import os
from setuptools import setup, Extension
from Cython.Build import cythonize

CWD = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(CWD,'src')
INCLUDE_DIR = os.path.join(os.path.split(CWD)[0],'gurls++/include')
LIB_DIR = os.path.join(os.path.split(CWD)[0],'build/lib')


def read(fname):
    return open(os.path.join(CWD, fname)).read()

#ext_modules = [Extension("pygurls", 
#                         ["src/pygurls.pyx","src/pygurls_wrapper.cpp"],                        
#                        include_dirs = [SRC_DIR,INCLUDE_DIR],                       
#                        library_dirs = [LIB_DIR],
#                        libraries=["libgurls++"])]

ext_modules = [Extension("pygurls", 
                         ["extension/pygurls.pyx","src/pygurls_wrapper.cpp"],                        
                        include_dirs = [SRC_DIR,INCLUDE_DIR],                       
                        library_dirs = [LIB_DIR],
                        libraries=["gurls++"],
                        language = "c++")]

setup(
    name="PyGURLS++",
    version="0.0.1",
    author="Pedro Santana",
    author_email="psantana@mit.edu",
    description="A Python wrapper for the GURLS++/bGURLS++ libraries.",
    long_description=read("README"), #Reads from README in the same folder
    ext_modules = cythonize(ext_modules,                           
                            include_path=[SRC_DIR,INCLUDE_DIR]))

#setup(
#    name="PyGURLS",
#    version="0.0.1",
#    author="Pedro Santana",
#    author_email="psantana@mit.edu",
#    description="A Python wrapper for the GURLS++/bGURLS++ libraries.",
#    long_description=read("README"), #Reads from README in the same folder
#    ext_modules = cythonize("pygurls.pyx",      
#                            source = ["pygurls_wrapper.cpp"],
#                            language="c++")    
#)

#setup(ext_modules = cythonize(
#            "pygurls.pyx", # our Cython source
#            sources=["../gurls++/src/options.cpp"],  # additional source file(s)
#            language="c++" # generate C++ code
#    ))
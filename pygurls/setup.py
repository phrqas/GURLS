#!/usr/bin/env python
#
#  A Python wrapper for GURLS++.
#
#  Copyright (c) 2015 Pedro Santana. All rights reserved.
#
#   author: Pedro Santana
#   e-mail: psantana@mit.edu
#   website: people.csail.mit.edu/psantana
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#  3. Neither the name Lily nor the names of its contributors may be
#     used to endorse or promote products derived from this software
#     without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
#  OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
#  AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
#  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.
#
"""
A Python wrapper for GURLS++

Setup file for compiling the project with Cython.

@author: Pedro Santana (psantana@mit.edu).
""" 
import os
from setuptools import setup, Extension
from Cython.Build import cythonize

CWD = os.path.abspath(os.path.dirname(__file__))
GURLS_ROOT = os.path.split(CWD)[0]

PYGURLS_SRC = os.path.join(CWD,'src')
GURLSPP_INCLUDE = os.path.join(GURLS_ROOT,'gurls++/include')
GURLSPP_LIB = os.path.join(GURLS_ROOT,'build/lib')


def read(fname):
    return open(os.path.join(CWD, fname)).read()

def file_list(folder,file_ext):  
    """Returns a list of files"""
    exts = (file_ext) if not isinstance(file_ext,(list,tuple)) else file_ext        
    return [os.path.join(folder,f)
                for f in os.listdir(folder) 
                    if os.path.isfile(os.path.join(folder,f)) 
                                and f.endswith(exts)]

#Do some sanity checking here to ensure that all files are in place.

ext_modules = [Extension("pygurls", 
                        file_list(folder='extension',file_ext='.pyx')+file_list(folder='src',file_ext='.cpp'),                        
                        include_dirs = [PYGURLS_SRC,GURLSPP_INCLUDE],                       
                        library_dirs = [GURLSPP_LIB],
                        libraries=["gurls++"],
                        language = "c++")]

setup(
    name="PyGURLS++",
    version="0.0.1",
    author="Pedro Santana",
    author_email="psantana@mit.edu",
    description="A Python wrapper for the GURLS++ libraries.",
    long_description=read("README"), #Reads from README in the same folder
    install_requires=['cython','numpy'],
    ext_modules = cythonize(ext_modules,                           
                            include_path=[PYGURLS_SRC,GURLSPP_INCLUDE]))


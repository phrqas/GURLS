#  A Python wrapper for GURLS++
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
A Python wrapper for GURLS++/bGURLS++

This is a Cython wrapper for allowing GURLS++/bGURLS++ functions to be called
from within Python.

@author: Pedro Santana (psantana@mit.edu).
""" 

cdef extern from "pygurls_wrapper.h" namespace "gurls":
    cdef cppclass PyGURLSWrapper:
        PyGURLSWrapper() except +
        
cdef class PyGURLS:
    cdef PyGURLSWrapper *thisptr # hold a C++ instance which we're wrapping
    def __cinit__(self):
        self.thisptr = new PyGURLSWrapper()
    def __dealloc__(self):
        del self.thisptr
    


#class PyGURLS(object):
#    """Wrapper class that encapsulates the funcionalities of GURLS into Python."""
#    def __init__(self):
#        #cdef PyGURLSWrapper *w = new PyGURLSWrapper(1)
#        print "You've created a pyGURLS wrapper object!"
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
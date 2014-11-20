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

"""
A Python wrapper for GURLS++

This is a Cython wrapper that allows GURLS++ functions to be called from 
natively from within Python.

@author: Pedro Santana (psantana@mit.edu).
""" 

#Declares the C++ wrapper class
cdef extern from "pygurls_wrapper.h" namespace "gurls":
    cdef cppclass PyGURLSWrapper:
        PyGURLSWrapper() except +
        void load_train_data(char*,char*) except +
        void load_test_data(char*,char*) except +
        void set_task_sequence(char*) except +
        void clear_task_sequence() except +
        void add_process(char*, char*) except +
        void init_processes(char*, bool) except +
        void clear_processes() except +
        void build_pipeline(char*, bool) except +
        int train(char*) except +
        int test(char*) except +
        int helloWorld() except +
        
        
cdef class PyGURLS:
    """Class that provides an Python interface to the functions in the C++
    wrapper class."""
    cdef PyGURLSWrapper *thisptr # hold a C++ instance which we're wrapping
    
    def __cinit__(self,*args,**kwargs):
        """Constructor for extension type."""
        self.thisptr = new PyGURLSWrapper() #Just declares a pointer
    
    def __dealloc__(self):
        """Destructor for extension type."""
        del self.thisptr
    
    def load_train_data(self,xtr_file,ytr_file):
        self.thisptr.load_train_data(xtr_file,ytr_file)
    
    def load_test_data(self,xte_file,yte_file):
        self.thisptr.load_test_data(xte_file,yte_file)
    
    def set_task_sequence(self,task_list):
        str_list = [p[0]+":"+p[1] for p in task_list]    
        self.thisptr.set_task_sequence("\n".join(str_list))
    
    def clear_task_sequence(self):
        self.thisptr.clear_task_sequence()
    
    def add_process(self,p_name,opt_str_list):
        self.thisptr.add_process(p_name,"\n".join(opt_str_list))
    
    def init_processes(self,p_name,use_default):        
        self.thisptr.init_processes(p_name,use_default)   
    
    def clear_processes(self):        
        self.thisptr.clear_processes()
    
    def build_pipeline(self,p_name,use_default):
        self.thisptr.build_pipeline(p_name,use_default)
    
    def train(self,job_id):
        return self.thisptr.train(job_id)    
        
    def test(self,job_id):
        return self.thisptr.test(job_id)
    
    def helloWorld(self):
        self.thisptr.helloWorld()
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

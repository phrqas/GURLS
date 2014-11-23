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
import numpy as np
cimport numpy as np
import scipy.io
from cython.view cimport array as cvarray
from libcpp.vector cimport vector


#Declares the C++ wrapper class
cdef extern from "pygurls_wrapper.h" namespace "gurls":
    cdef cppclass PyGURLSWrapper:
        PyGURLSWrapper() except +               
        PyGURLSWrapper(char*) except +
        const vector[double] get_acc() except +
        const vector[double] get_pred() except +
        void add_data(vector[double]&, unsigned long, unsigned long, char*) except +             
        void load_data(char*, char*) except +             
        vector[double] get_data_vec(char*) except +
        void erase_data(char*) except +
        void set_task_sequence(char*) except +
        void clear_task_sequence() except +
        void add_process(char*, char*) except +
        void init_processes(char*, bool) except +
        void clear_processes() except +
        void build_pipeline(char*, bool) except +
        void clear_pipeline() except +
        int  run(char*, char*, char*) except +   
        unsigned long get_num_rows() except +
        unsigned long get_num_cols() except +
        
        
cdef class PyGURLS:
    """Class that provides an Python interface to the functions in the C++
    wrapper class."""
    cdef PyGURLSWrapper *thisptr
        
    def __cinit__(self,data_type=None,*args,**kwargs):
        """Constructor for extension type."""        
        #Initializes the GURLS++ wrapper object and reference appropriately        
        if data_type != None:
            self.thisptr = new PyGURLSWrapper(data_type) 
        else:
            self.thisptr = new PyGURLSWrapper() 
            
    def __dealloc__(self):
        """Destructor for extension type."""
        del self.thisptr
    
    def _gMat2D_to_np(self,gMat2D_vec):
        vec_mat = np.array(gMat2D_vec)
        rows = self.thisptr.get_num_rows();
        cols = self.thisptr.get_num_cols();       
        if rows>1 and cols>1: 
            return vec_mat.reshape((rows,cols),order='F')
        else:
            return vec_mat
    
    property acc:
        def __get__(self):            
            return self._gMat2D_to_np(self.thisptr.get_acc())
                        
    property pred:
        def __get__(self):            
            return self._gMat2D_to_np(self.thisptr.get_pred())
                             
    def add_data(self,np.ndarray[np.float64_t, ndim=2] mat2D, data_id):
        cdef vector[double] vec_mat = mat2D.flatten('F')       
        self.thisptr.add_data(vec_mat,
                              <unsigned long>mat2D.shape[0],
                              <unsigned long>mat2D.shape[1],
                              data_id)             
             
    def load_data(self,data_file,data_id):        
        if data_file.endswith('.mat'): #MATLAB import
            data_dic = scipy.io.loadmat(data_file)
            var_loaded = []
            for var_name, mat in data_dic.iteritems():
                if not var_name.startswith('__'): #Ignores hidden variables
                    self.add_data(mat.astype(np.dtype('float64'),copy=False),
                                  var_name)
                    var_loaded.append(var_name)
            return var_loaded #Returns the names of the variables
        else: #Calls the C++ loading function for everything else                        
            self.thisptr.load_data(data_file,data_id)         

    def get_data(self,data_id):
        return self._gMat2D_to_np(self.thisptr.get_data_vec(data_id))        
        
    def erase_data(self,data_id):
        self.thisptr.erase_data(data_id)        
        
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
    
    def clear_pipeline(self):
        self.thisptr.clear_pipeline()
    
    def run(self,in_data_id, out_data_id, job_id):
        return self.thisptr.run(in_data_id,out_data_id,job_id)    
        
    
        
        
        
        
        
        

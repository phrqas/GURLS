#!/usr/bin/env python
#
#  A Python wrapper for GURLS++.
#
#  Copyright (c) 2014 MIT. All rights reserved.
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
#  3. Neither the name(s) of the copyright holders nor the names of its 
#     contributors or of the Massachusetts Institute of Technology may be 
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
A Python wrapper for GURLS++.

Cython wrapper that allows GURLS++ to be called natively from within Python.

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
        const vector[double] get_opt_field(char*,char*) except +        
        const vector[double] get_field(char*) except +
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
    """Class that provides a Python interface to GURLS++."""
    cdef PyGURLSWrapper *thisptr
        
    def __cinit__(self,data_type=None,*args,**kwargs):
        """Constructor.

        Optional arguments:
        data_type -- either 'double' (default) or 'float'
        """        
                
        if data_type != None:
            self.thisptr = new PyGURLSWrapper(data_type) 
        else:
            self.thisptr = new PyGURLSWrapper() 
            
    def __dealloc__(self):
        """Destructor."""
        
        del self.thisptr
    
    def _gMat2D_to_np(self,gMat2D_vec):
        """Convert from gMat2D type (GURLS++) to 2D NumPy array."""
        
        vec_mat = np.array(gMat2D_vec)
        rows = self.thisptr.get_num_rows();
        cols = self.thisptr.get_num_cols();         
        if (rows > 1) and (cols > 1):
            return vec_mat.reshape((rows,cols),order='F')        
        else:
            return vec_mat
    
    def get_field(self,field):    
        """Return field within a GurlsOptionsList structure."""        
        
        return self._gMat2D_to_np(self.thisptr.get_field(field))
    
    def get_option_field(self,option,field):
        """Return field within nested option in a GurlsOptionsList structure."""        
        
        return self._gMat2D_to_np(self.thisptr.get_opt_field(option,field))
                         
    def add_data(self,mat2D, data_id):
        """Add 2D NumPy array to GURLS++ pipeline with id=data_id."""
        
        mat = np.reshape(mat2D,(mat2D.shape[0],1)) if len(mat2D.shape) == 1 else mat2D
                
        cdef vector[double] vec_mat = mat.flatten('F')       
        self.thisptr.add_data(vec_mat,
                              <unsigned long>mat.shape[0],
                              <unsigned long>mat.shape[1],
                              data_id)             
             
    def load_data(self,data_file,data_id):                
        """Load file=data_file and add to GURLS++ pipeline with id=data_id."""
                
        self.thisptr.load_data(data_file,data_id)         

    def import_mat_file(self,mat_file,var_names=[]):           
        """Load MATLAB workspace file mat_file as Python dictionary.
        
        Optional arguments:        
        var_names -- list of variable names to be imported (all by default).
        """
                
        if len(var_names)>0:
            data_dic = scipy.io.loadmat(mat_file,appendmat=True,
                                        variable_names=var_names)
        else:
            data_dic = scipy.io.loadmat(mat_file,appendmat=True)        
        return data_dic 
    
    def get_data(self,data_id):
        """Retrieve 2D matrix from GURLS++ with id=data_id as NumPy array."""        
        
        return self._gMat2D_to_np(self.thisptr.get_data_vec(data_id))        
        
    def erase_data(self,data_id):
        """Remove 2D matrix from GURLS++ with id=data_id."""
        
        self.thisptr.erase_data(data_id)        
        
    def set_task_sequence(self,task_list):
        """Set the sequence of tasks in the GURLS++ opt. pipeline.
        
        task_list = [ ['opt_1','arg_1'], ['opt_2','arg_2'], ... ]        
        """
        
        str_list = [p[0]+":"+p[1] for p in task_list]    
        self.thisptr.set_task_sequence("\n".join(str_list))
    
    def clear_task_sequence(self):
        """Clear the sequence of tasks in the GURLS++ opt. pipeline."""
        
        self.thisptr.clear_task_sequence()
    
    def add_process(self,p_name,opt_str_list):
        """Add an optimization process to GURLS++."""
        
        self.thisptr.add_process(p_name,"\n".join(opt_str_list))
    
    def init_processes(self,p_name,use_default):     
        """Initialize list of GURLS++ optimization processes."""
        
        self.thisptr.init_processes(p_name,use_default)   
    
    def clear_processes(self):        
        """Clear list of GURLS++ optimization processes."""
        
        self.thisptr.clear_processes()
    
    def build_pipeline(self,p_name,use_default):
        """Build the GURLS++ optimization pipeline."""
        
        self.thisptr.build_pipeline(p_name,use_default)
    
    def clear_pipeline(self):
        """Clear the GURLS++ optimization pipeline."""
        
        self.thisptr.clear_pipeline()
    
    def run(self,in_data_id, out_data_id, job_id):
        """Run a process with given input and output data.
        
        Mandatory arguments:
        in_data_id -- string id of the input data.
        out_data_id -- string id of the output data.
        job_id -- string id of the process to be executed.   
        """
        
        return self.thisptr.run(in_data_id,out_data_id,job_id)    
        
    
        
        
        
        
        
        

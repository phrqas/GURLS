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

Converts the Statlog (Landsat Satellite) data set into a MATLAB .mat file 
containing the standard names Xtrain, Ytrain, Xtest, Ytest.

@author: Pedro Santana (psantana@mit.edu).
""" 
import numpy as np
import scipy.io

ws = {}
sat_train = np.loadtxt('sat.trn')
sat_test = np.loadtxt('sat.tst')

ws['Xtrain'] = sat_train[:,:-1] #Training inputs are all, but last column
ws['Ytrain'] = sat_train[:,-1]  #Training outputs are the last column
ws['Xtest'] = sat_test[:,:-1] #Testing inputs are all, but last column
ws['Ytest'] = sat_test[:,-1]  #Testing outputs are the last column

scipy.io.savemat('landsat',ws,oned_as='column')
    
    
    
    
    
    
    
    
    
    
 
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
A Python wrapper for GURLS++

An implementation of helloworld.cpp using PyGURLS

@author: Pedro Santana (psantana@mit.edu).
"""
import numpy as np
import pygurls
import sys
import os

#Checks path 
if len(sys.argv) != 2:           
        print "Usage: "+sys.argv[0]+" <path to gurls++ data directory>"        
        sys.exit()

mat_file = os.path.join(sys.argv[1],'ps1-dataset.mat') #MAT file

# python object that handles the interface with GURLS++
pg = pygurls.PyGURLS(data_type='double')

print "Importing MATLAB workspace from "+mat_file
mat_dic = pg.import_mat_file(mat_file)

# Converts the desired variables to double
Xtrain = mat_dic['Xtrain'].astype(np.dtype('float64'),copy=False)
Ytrain = mat_dic['Ytrain'].astype(np.dtype('float64'),copy=False)
Xtest = mat_dic['Xtest'].astype(np.dtype('float64'),copy=False)
Ytest = mat_dic['Ytest'].astype(np.dtype('float64'),copy=False)

print "Centering training and testing sets."
Xtr_mean = np.mean(Xtrain,axis=0)
Ytr_mean = np.mean(Ytrain,axis=0)

Xtrain_center = Xtrain - Xtr_mean 
Ytrain_center = Ytrain - Ytr_mean
Xtest_center = Xtest - Xtr_mean 
Ytest_center = Ytest - Ytr_mean

print "Adding data to GURLS++."
pg.add_data(Xtrain,'Xtrain')
pg.add_data(Xtrain_center,'Xtrain_center')
pg.add_data(Ytrain,'Ytrain')
pg.add_data(Ytrain_center,'Ytrain_center')
pg.add_data(Xtest,'Xtest')
pg.add_data(Xtest_center,'Xtest_center')
pg.add_data(Ytest,'Ytest')
pg.add_data(Ytest_center,'Ytest_center')

print "Building and running the optimization problem."
# specify the task sequence         
task_list = [['kernel','linear'],['paramsel','loocvdual'],['optimizer','rlsdual'],
           ['pred','dual'],['perf','macroavg']]

pg.set_task_sequence(task_list)

# initializes the list of processes with default options
pg.init_processes('processes',True)

# defines instructions for training
opt_str_list = ['computeNsave','computeNsave','computeNsave','ignore','ignore']
pg.add_process('train_process',opt_str_list)

# defines instructions for evaluatng performance
opt_str_list = ['load','load','load','computeNsave','computeNsave']
pg.add_process('eval_perf',opt_str_list)

# builds the GURLS++ optimization pipeline
pg.build_pipeline('matlab_demo', True)

# runs the training process with training data
pg.run('Xtrain','Ytrain','train_process')
# evaluates performance on testing data
pg.run('Xtest','Ytest','eval_perf')
acc_uncenter = pg.get_option_field('perf','acc')

# runs the training process with training data
pg.run('Xtrain_center','Ytrain_center','train_process')
# evaluates performance on testing data
pg.run('Xtest_center','Ytest_center','eval_perf')
acc_center = pg.get_option_field('perf','acc')

print "(Uncentered data) Accuracy on testing set= %.6f"%(acc_uncenter)
print "(Centered data) Accuracy on testing set= %.6f"%(acc_center)










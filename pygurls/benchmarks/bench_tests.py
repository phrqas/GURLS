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

Module defining the different types of tests that can be executed.

@author: Pedro Santana (psantana@mit.edu).
""" 
import numpy as np
import pygurls
import sklearn.svm
import sklearn.linear_model


def pygurls_gaussian_kernel(Xtrain,Ytrain,Xtest,Ytest,*args,**kwargs):
    """RBF kernel."""
    pg = pygurls.PyGURLS(data_type='double')

    pg.add_data(Xtrain,'Xtrain'); pg.add_data(Ytrain,'Ytrain')
    pg.add_data(Xtest,'Xtest'); pg.add_data(Ytest,'Ytest')

    task_list = [['paramsel','siglam'],['kernel','rbf'],['optimizer','rlsdual'],
             ['predkernel','traintest'],['pred','dual'],['perf','macroavg']]
    pg.set_task_sequence(task_list)
    
    pg.init_processes('processes',True)
    
    opt_str_list = ['computeNsave','computeNsave','computeNsave','ignore','ignore',
                'ignore']
    pg.add_process('train_process',opt_str_list)    
    
    opt_str_list = ['load','load','load','computeNsave','computeNsave',
                'computeNsave']
    pg.add_process('eval_perf',opt_str_list)
    
    pg.build_pipeline('pygurls_rbf_bench', True)
    
    pg.run('Xtrain','Ytrain','train_process')
    pg.run('Xtest','Ytest','eval_perf')
    
    return pg.get_option_field('perf','acc')[0]

def pygurls_linear_primal(Xtrain,Ytrain,Xtest,Ytest,*args,**kwargs):
    """Linear kernel (primal)."""
    pg = pygurls.PyGURLS(data_type='double')    
    
    Xtr_mean = np.mean(Xtrain,axis=0) #Centers the data
    Ytr_mean = np.mean(Ytrain,axis=0)    
    Xtrain_center = Xtrain - Xtr_mean 
    Ytrain_center = Ytrain - Ytr_mean
    Xtest_center = Xtest - Xtr_mean 
    Ytest_center = Ytest - Ytr_mean
    
    pg.add_data(Xtrain_center,'Xtrain'); pg.add_data(Ytrain_center,'Ytrain')
    pg.add_data(Xtest_center,'Xtest'); pg.add_data(Ytest_center,'Ytest')
    
#    task_list = [['kernel','linear'],['paramsel','loocvprimal'],['optimizer','rlsprimal'],
#           ['pred','primal'],['perf','macroavg']]
    task_list = [['split','ho'],['paramsel','hoprimal'],['optimizer','rlsprimal'],
           ['pred','primal'],['perf','macroavg']]
    pg.set_task_sequence(task_list)
    
    pg.init_processes('processes',True)

    opt_str_list = ['computeNsave','computeNsave','computeNsave','ignore','ignore']
    pg.add_process('train_process',opt_str_list)
    
    opt_str_list = ['load','load','load','computeNsave','computeNsave']
    pg.add_process('eval_perf',opt_str_list)
    
    pg.build_pipeline('pygurls_lin_bench', True)
    
    pg.run('Xtrain','Ytrain','train_process')
    pg.run('Xtest','Ytest','eval_perf')
    
    return pg.get_option_field('perf','acc')[0]


def sklearn_SVC_linear(Xtrain,Ytrain,Xtest,Ytest,*args,**kwargs):
    clf = sklearn.svm.SVC(kernel='linear')    
    clf.fit(Xtrain,Ytrain)
    return clf.score(Xtest,Ytest)

def sklearn_SVC_rbf(Xtrain,Ytrain,Xtest,Ytest,*args,**kwargs):
    clf = sklearn.svm.SVC(kernel='rbf')    
    clf.fit(Xtrain,Ytrain)
    return clf.score(Xtest,Ytest)

def sklearn_linear_SVC_primal(Xtrain,Ytrain,Xtest,Ytest,*args,**kwargs):
    clf = sklearn.svm.LinearSVC(dual=False,fit_intercept=True)
    clf.fit(Xtrain,Ytrain)
    return clf.score(Xtest,Ytest)

def sklearn_linear_SVC_dual(Xtrain,Ytrain,Xtest,Ytest,*args,**kwargs):
    clf = sklearn.svm.LinearSVC(dual=True,fit_intercept=True)
    clf.fit(Xtrain,Ytrain)
    return clf.score(Xtest,Ytest)
    
def sklearn_ridge_cv(Xtrain,Ytrain,Xtest,Ytest,*args,**kwargs):
    clf = sklearn.linear_model.RidgeClassifierCV(fit_intercept=True)
    clf.fit(Xtrain,Ytrain)
    return clf.score(Xtest,Ytest)
    
    
    
    
    
    
    
    
 
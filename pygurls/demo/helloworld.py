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

An implementation of helloworld.cpp using PyGURLS

@author: Pedro Santana (psantana@mit.edu).
"""
import pygurls
import sys
import os

#Checks path 
if len(sys.argv) != 2:           
        print "Usage: "+sys.argv[0]+" <path to gurls++ data directory>"        
        sys.exit()

# python object that handles the interface with GURLS++
pg = pygurls.PyGURLS(data_type='double')

# load data from files specified as command-line arguments
pg.add_data(os.path.join(sys.argv[1],'Xtr.txt'),'xtr')
pg.add_data(os.path.join(sys.argv[1],'ytr_onecolumn.txt'),'ytr')
pg.add_data(os.path.join(sys.argv[1],'Xte.txt'),'xte')
pg.add_data(os.path.join(sys.argv[1],'yte_onecolumn.txt'),'yte')

# specify the task sequence
task_list = [['kernel','linear'], ['paramsel','loocvdual'],
             ['optimizer','rlsdual'],['pred','dual'],['perf','macroavg']]

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
pg.build_pipeline('helloworld', True)

# runs the training process with training data
pg.run('xtr','ytr','train_process')

# evaluates performance on testing data
pg.run('xte','yte','eval_perf')

print pg.acc










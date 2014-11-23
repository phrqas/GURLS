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

Demonstrates data I/O using NumPy and GURLS++

@author: Pedro Santana (psantana@mit.edu).
"""
import pygurls
import numpy as np
import sys
import os

#Checks path 
if len(sys.argv) != 2:           
        print "Usage: "+sys.argv[0]+" <path to gurls++ data directory>"        
        sys.exit()

print "Demonstrates data I/O using NumPy and GURLS++\n"

# python object that handles the interface with GURLS++
pg = pygurls.PyGURLS(data_type='double')

print "Loading data from files in "+sys.argv[1]
pg.load_data(os.path.join(sys.argv[1],'Xtr.txt'),'xtr')
pg.load_data(os.path.join(sys.argv[1],'Xte.txt'),'xte')
pg.load_data(os.path.join(sys.argv[1],'ytr_onecolumn.txt'),'ytr')
pg.load_data(os.path.join(sys.argv[1],'yte_onecolumn.txt'),'yte')

print "Importing data files from GURLS++ into NumPy matrices"
xtr = pg.get_data('xtr')
xte = pg.get_data('xte')
ytr = pg.get_data('ytr')
yte = pg.get_data('yte')

print "Concatenating training and testing data\n"
x_total = np.vstack((xtr,xte))
y_total = np.vstack((ytr,yte))

print "Total input data (rows,cols)=(%d,%d)"%(x_total.shape[0],x_total.shape[1])
print "Input output data (rows,cols)=(%d,%d)\n"%(y_total.shape[0],y_total.shape[1])

print "Adding concatenated NumPy matrices into GURLS++"
pg.add_data(x_total,'x_total')
pg.add_data(y_total,'y_total')

print "Retrieving a copy of the data that was just added\n"
x_total_cp = pg.get_data('x_total')
y_total_cp = pg.get_data('y_total')

#Total data I/O error
x_dev = np.sum(np.sum(np.abs(x_total-x_total_cp)))
y_dev = np.sum(np.sum(np.abs(y_total-y_total_cp)))

print "Total absolute I/O deviation (X,y)=(%.6f,%.6f)"%(x_dev,y_dev)













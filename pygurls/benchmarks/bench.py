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

Sets up the benchmarking scripts based on the configuration file.

@author: Pedro Santana (psantana@mit.edu).
""" 
import misc
import time
import os
import re
import scipy.io

def read_bench_config(config_file='config_benchmarks.txt'):    
    """Read the benchmark configuration file."""
    learning_func_dict={}            
    with open(config_file,'r') as f_conf:         
        for line in f_conf:
            line_trim = line.strip(' \t\n')
            if (len(line_trim) == 0) or (len(line_trim)>0 and line_trim[0]=='#'): 
                continue         
            tokens = re.split(' * |\t*\t',line_trim) #any tabs and spaces
            if len(tokens)<3:
                raise Exception('Line format error. Usage: <learn-fcn> <n-runs> <ds1> <ds2> ...') 
            if not tokens[1].isdigit():
                raise Exception('Second parameter should be the number of runs.')                 

            learning_func_dict[tokens[0]]={'nruns':tokens[1],'datasets':tokens[2:]}
            
    return learning_func_dict                                 
                 
def generate_bench_code(config_file='config_benchmarks.txt',force_datasets=False):
    """Genereate code that runs all benchmarks."""    
    #Loads datasets
    mat_file_dict,error = misc.generate_datasets(force=force_datasets)     
    if not error:                 
        #Loads benchmark configuration
        learning_func_dict = read_bench_config(config_file)
        
        for func_name,param_dic in learning_func_dict.iteritems():          
            if len(param_dic['datasets']) == 1 and param_dic['datasets'][0] == '_all_':
                param_dic['datasets'] = [os.path.join(v,k) for k,v in mat_file_dict.iteritems()]
            else:
                #Adds path to data set name
                for i,dset in enumerate(param_dic['datasets']):
                    if dset in mat_file_dict.keys():                        
                        full_path = os.path.join(mat_file_dict[dset],dset)
                        param_dic['datasets'][i] = full_path     
                    else:
                        raise Exception('Data set '+dset+' not found.')        
        #Writes a Python script that runs all desired tests
        #(if only Python had macros...)
        write_run_script(learning_func_dict)
    else:
        raise Exception('Failed to load the data sets.')

def write_run_script(learning_func_dict):
    with open('bench_run.py','w') as f_run:
        f_run.write('#!/usr/bin/env python\n') #shebang
        f_run.write('#--Automatically generated by bench.py. Any changes will be discarded.\n')        
        f_run.write('from bench import benchmark\n')
        f_run.write('from bench_tests import *\n\n')
        
        for func_name,param_dic in learning_func_dict.iteritems(): 
            for dset in param_dic['datasets']:
                bench_str = 'benchmark(mat_file=\"'+dset+'\",'
                bench_str +='learning_func='+func_name+','                
                bench_str += 'n_runs='+str(param_dic['nruns'])+','
                bench_str += 'msg='+'\"Running '+func_name+' on '
                bench_str += os.path.split(dset)[1]+'\")\n'           
                f_run.write(bench_str)
            
def benchmark(mat_file,learning_func,n_runs=1,msg=''):
    """Benchmark a learning algorithm."""
    print msg #Prints optional message
    ws = scipy.io.loadmat(mat_file,squeeze_me=True) #Loads data set    
    elap_list=[]; perf_list=[]
    for n in range(n_runs):            
        start = time.time()         
        perf = learning_func(Xtrain=ws['Xtrain'],
                             Ytrain=ws['Ytrain'],
                             Xtest=ws['Xtest'],
                             Ytest=ws['Ytest'])        
        elap_list.append(time.time()-start)
        perf_list.append(perf)
    return elap_list,perf_list


if __name__ == '__main__':
    generate_bench_code(config_file='config_benchmarks.txt',force_datasets=False)    

    

    
    
    
    
    
    
    
    
 
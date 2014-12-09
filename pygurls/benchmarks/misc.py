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

Miscellaneous functions for benchmarking pyGURLS.

@author: Pedro Santana (psantana@mit.edu).
""" 
import os   
import fnmatch as fn

def has_file_pattern(file_list,pattern):
    for filename in file_list:
        if fn.fnmatch(filename,pattern):
            return filename
    return None

def cprint(pstring,cond):
    if cond:
        print pstring        

def generate_datasets(dataset_folder='./datasets',verbose=False,force=False):
    """Return dictionary of datasets mapping to their paths."""
    sep='-->'       
    mat_file_dict={}
    error_flag=False
    for folder,subfolders,filenames in os.walk(dataset_folder): 
        cprint(sep+folder,verbose)    

        pp_script = has_file_pattern(filenames,'pre_process*.py')
        mat_file = has_file_pattern(filenames,'*.mat')
        
        if pp_script != None:
            if mat_file == None or force:
                cprint(' '*(len(sep)+2)+'Executing script '+pp_script,verbose)                           
                cwd = os.getcwd()                        
                os.chdir(folder)            
                os.system('python '+pp_script)
                mat_file = has_file_pattern(os.listdir('.'),'*.mat')                
                if mat_file != None:
                    mat_file_dict[mat_file] = os.path.abspath('.')                    
                    cprint(' '*(len(sep)+2)+'Matlab file '+mat_file+' successfully generated.',verbose)                             
                else:
                    error_flag = True
                    cprint(' '*(len(sep)+2)+'ERROR: failed to generated Matlab file in '+folder,verbose)
                    
                os.chdir(cwd)            
            else:
                mat_file_dict[mat_file] = os.path.abspath(folder)                
                cprint(' '*(len(sep)+2)+'Found '+mat_file+'. Skipping script '+pp_script,verbose)
                 
    return mat_file_dict,error_flag #Returns the list of generated mat files
   
   
def print_benchmark_results(results_dict,sep='   '):
    methods = results_dict.keys()
    datasets = set()
    for m in results_dict.keys(): 
        for ds in results_dict[m].keys():
            datasets.add(ds)
    datasets = list(datasets)
    
    results_table = [['' for j in range(len(datasets))] for i in range(len(methods))]
    for i,m in enumerate(methods):        
        for j,ds in enumerate(datasets):        
            if ds in results_dict[m].keys():
                results_table[i][j] ='%.2f   %.4f'%(results_dict[m][ds]['perf'][0]*100.0,
                                      results_dict[m][ds]['elap'][0])
            else:
                results_table[i][j] ='---   ---'            

    max_len_method = max([len(m) for m in methods]+[len('Method')])
    max_len_dataset = max([len(d) for d in datasets]+[len('perf(%)   elap(s)')])
    max_len_result=-1
    for i in range(len(methods)):
        for j in range(len(datasets)):
            if len(results_table[i][j])>max_len_result:
                max_len_result = len(results_table[i][j])
    max_col_width = max([max_len_dataset,max_len_result])
   
    #Table of results
    bench_str=''
    #Header   
    bench_str+='Method'+' '*(max_len_method-len('Method'))+sep 
    for ds in datasets:
        bench_str+= ds+' '*(max_col_width-len(ds))+sep                   
    bench_str+='\n'
    bench_str+=(' '*max_len_method)+sep
    for i in range(len(datasets)):
        bench_str+='perf(%)   elap(s)'+' '*(max_col_width-len('perf(%)   elap(s)'))+sep
    bench_str+='\n'
    bench_str+=('#'*max_len_method+sep)+('#'*max_col_width+sep)*len(datasets)+'\n'
                        
    for i,m in enumerate(methods):
        bench_str+= m+' '*(max_len_method-len(m))+sep
        for j,ds in enumerate(datasets):
            bench_str+= results_table[i][j]+' '*(max_col_width-len(results_table[i][j]))+sep            
        bench_str+='\n'
        
    print bench_str  
    return bench_str

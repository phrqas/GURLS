/*
 * A Python wrapper for GURLS++.
 *
 * Copyright (c) 2015 Pedro Santana. All rights reserved.
 *
 * author: Pedro Santana
 * e-mail: psantana@mit.edu
 * website: people.csail.mit.edu/psantana
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 * 3. Neither the name Lily nor the names of its contributors may be
 *    used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 * COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
 * OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
 * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 * ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */
#include <iostream> 
#include <stdexcept>
#include <string>
#include <string.h>

#include "gurls++/gurls.h"
#include "gurls++/traintest.h"
#include "gurls++/exceptions.h"
#include "gurls++/gvec.h"
#include "gurls++/gmat2d.h"
#include "gurls++/options.h"
#include "gurls++/optlist.h"
#include "gurls++/gmath.h"

namespace gurls {
       
    class PyGURLSWrapper {
    private:
        GURLS G;
        std::map< char*, gMat2D<double>* > data_map;        
        OptTaskSequence *seq; // task sequence        
        GurlsOptionsList *processes; //GURLS processes
        GurlsOptionsList *opt; // options structure
    public:
        PyGURLSWrapper();
        ~PyGURLSWrapper();
        void add_data(char* data_file, char* data_id);     
        void erase_data(char* data_id);
        void clear_data();
        void set_task_sequence(char* seq_str);
        void clear_task_sequence();
        void add_process(char* p_name, char* opt_str);        
        void init_processes(char* p_name, bool use_default);
        void clear_processes();
        void build_pipeline(char* p_name, bool use_default);
        void clear_pipeline();
        int  run(char* in_data, char* out_data, char* job_id);      
    };
}



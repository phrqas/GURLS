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
 
#include "pygurls_wrapper.h"

using namespace std;
using namespace gurls;

/**
 *@brief: Default constructor assumes double as the data type
 */
PyGURLSWrapper::PyGURLSWrapper()
{
    this->seq = NULL;
    this->processes = NULL;    
    this->opt = NULL;

    this->pt_run = &gurls::PyGURLSWrapper::run_double;
    this->pt_load_data = &gurls::PyGURLSWrapper::load_data_double;
}

/**
 *@brief: Typed constructor selects correct data-handling functions.
 */
PyGURLSWrapper::PyGURLSWrapper(char* data_type)
{
    this->seq = NULL;
    this->processes = NULL;    
    this->opt = NULL;    

    if (strcmp(data_type,"double") == 0)
    {
        this->pt_run = &gurls::PyGURLSWrapper::run_double;
        this->pt_load_data = &gurls::PyGURLSWrapper::load_data_double;
    }
    else if (strcmp(data_type,"float") == 0)
    {
        this->pt_run = &gurls::PyGURLSWrapper::run_float;
        this->pt_load_data = &gurls::PyGURLSWrapper::load_data_float;
    }
    else
        throw std::runtime_error("Type "+std::string(data_type)+" not currently supported.");
}
 
PyGURLSWrapper::~PyGURLSWrapper()
{
    this->clear_pipeline();    
}
 
const std::vector<double> PyGURLSWrapper::export_gmat(const gMat2D<double>& mat)
{
    this->num_mat_rows = mat.rows();       
    this->num_mat_cols = mat.cols();
    return std::vector<double>(mat.begin(),mat.end());
}
 
void PyGURLSWrapper::load_data(char* data_file, char* data_id)
{
    (*this.*pt_load_data)(data_file,data_id);
}

void PyGURLSWrapper::load_data_double(char* data_file, char* data_id)
{
    gMat2D<double> *pdata = new gMat2D<double>();             
    pdata->readCSV(data_file); //loads data from file    
    this->data_map[data_id] = pdata; //stores the reference
}

void PyGURLSWrapper::load_data_float(char* data_file, char* data_id)
{
    gMat2D<float> *pdata = new gMat2D<float>();             
    pdata->readCSV(data_file); //loads data from file    
    this->data_map[data_id] = pdata; //stores the reference
}
 
void PyGURLSWrapper::add_data(std::vector<double>& vec_dat, unsigned long rows, 
                                unsigned long cols,char* data_id)
{
    gMat2D<double> *pdata = new gMat2D<double>(vec_dat.data(),rows,cols,true);                 
    this->data_map[data_id] = pdata; //stores the reference
}

std::vector<double> PyGURLSWrapper::get_data_vec(char* data_id)
{
    gMat2D<double> *pdata = (gMat2D<double>*) this->data_map[data_id];
    return export_gmat(*pdata);    
}

void PyGURLSWrapper::erase_data(char* data_id)
{    
    delete this->data_map[data_id]; //deallocates the data
    this->data_map.erase(data_id); 
}

const std::vector<double> PyGURLSWrapper::get_field(char* field)
{
    const gMat2D<double>& mat 
        = OptMatrix<gMat2D<double> >::dynacast(this->opt->getOpt(field))->getValue();
    return export_gmat(mat);        
}

const std::vector<double> PyGURLSWrapper::get_opt_field(char* option,char* field)
{    
    GurlsOptionsList* perf = GurlsOptionsList::dynacast(this->opt->getOpt(option));
    GurlsOption *perf_field = perf->getOpt(field);  
    
    //Hack to deal with the fact that sigma is stored as a double, rather
    //than a gMat2D.
    if((strcmp(option,"paramsel")==0)&&(strcmp(field,"sigma")==0))
    {
        double sigma = this->opt->getOptValue<OptNumber>("paramsel.sigma");
        gMat2D<double> *pmat = new gMat2D<double>(&sigma,1,1,true);                 
        return export_gmat(*pmat);        
    }
    else
    {
        const gMat2D<double>& mat = OptMatrix<gMat2D<double> >::dynacast(perf_field)->getValue();          
        return export_gmat(mat);        
    }
}

void PyGURLSWrapper::set_task_sequence(char* seq_str)
{
    char *token;

    this->clear_task_sequence();    
    this->seq = new OptTaskSequence();
        
    token = strtok (seq_str,"\n");
    while (token != NULL)
    {   
        *(this->seq) << string(token);
        token = strtok (NULL,"\n");
    }
}

 
void PyGURLSWrapper::clear_task_sequence()
{
    if (this->seq != NULL)
    {
        delete this->seq;
        this->seq = NULL;
    }
} 

 
void PyGURLSWrapper::add_process(char* p_name, char* opt_str)
{
    char *token; //Tokens from the option string
    
    if (this->processes == NULL)
        throw std::runtime_error("Initialize before adding processes.");

    OptProcess* opt_process = new OptProcess(); //new optimization process

    token = strtok (opt_str,"\n");
    while (token != NULL)
    {   
        if (strcmp(token,"computeNsave") == 0)
            *opt_process << GURLS::computeNsave;
        else if (strcmp(token,"ignore") == 0)
            *opt_process << GURLS::ignore;
        else if (strcmp(token,"load") == 0)
            *opt_process << GURLS::load;   
        else if (strcmp(token,"compute") == 0)
            *opt_process << GURLS::compute;
        else if (strcmp(token,"remove") == 0)
            *opt_process << GURLS::remove;         
        else
            throw std::runtime_error(std::string(token)+": unsupported action.");

        token = strtok (NULL,"\n"); //Next token
    }        
    this->processes->addOpt(p_name,opt_process);//Adds to current process list
}

 
void PyGURLSWrapper::clear_processes()
{
    if (this->processes != NULL)
    {
        delete this->processes;
        this->processes = NULL;
    }
}

 
void PyGURLSWrapper::init_processes(char* p_name, bool use_default)
{
    this->clear_processes();   
    this->processes = new GurlsOptionsList(p_name, use_default);
}

 
void PyGURLSWrapper::build_pipeline(char* p_name, bool use_default)
{
    if (this->seq == NULL)
        throw std::runtime_error("Empty task sequence!");
    if (this->processes == NULL)
        throw std::runtime_error("Empty list of processes!");

    // builds the GURLS++ pipeline
    this->opt = new GurlsOptionsList(p_name, use_default);
    this->opt->addOpt("seq", this->seq);
    this->opt->addOpt("processes", this->processes);
}

 
void PyGURLSWrapper::clear_pipeline()
{
    //TODO: fix the segmentation fault here when we call the code twice
    //this->clear_task_sequence();
    //this->clear_processes();
    
    if (this->opt != NULL)
    {
        delete this->opt;
        this->opt = NULL;
    }
}


int PyGURLSWrapper::run(char* in_data, char* out_data, char* job_id)
{
    return (*this.*pt_run)(in_data,out_data,job_id);
}

int PyGURLSWrapper::run_double(char* in_data, char* out_data, char* job_id)
{
    try{        
        this->G.run(*((gMat2D<double>*)this->data_map[in_data]),
                    *((gMat2D<double>*)this->data_map[out_data]),
                    *(this->opt), 
                    job_id);
        return EXIT_SUCCESS;
    }
    catch(gException& e){
        cout << e.getMessage() << endl;
        return EXIT_FAILURE;
    }
}

int PyGURLSWrapper::run_float(char* in_data, char* out_data, char* job_id)
{
    try{        
        this->G.run(*((gMat2D<float>*)this->data_map[in_data]),
                    *((gMat2D<float>*)this->data_map[out_data]),
                    *(this->opt), 
                    job_id);
        return EXIT_SUCCESS;
    }
    catch(gException& e){
        cout << e.getMessage() << endl;
        return EXIT_FAILURE;
    }
}




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

PyGURLSWrapper::PyGURLSWrapper()
{
    this->seq = NULL;
    this->processes = NULL;    
    this->opt = NULL;    
}

PyGURLSWrapper::~PyGURLSWrapper()
{
    //this->clear_pipeline();
    //this->clear_data();
}

void PyGURLSWrapper::add_data(char* data_file, char* data_id)
{
    gMat2D<double> *pdata = new gMat2D<double>(); //new container
    pdata->readCSV(data_file); //loads data from file    
    this->data_map[data_id] = pdata; //stores the reference
}

void PyGURLSWrapper::erase_data(char* data_id)
{
    delete this->data_map[data_id]; // deallocates the data
    this->data_map.erase(data_id); // removes the reference
}

void PyGURLSWrapper::clear_data()
{    
    // deallocates all data
    std::map< char*, gMat2D<double>* >::iterator it;
    for(it = this->data_map.begin(); it != this->data_map.end(); ++it)
        delete this->data_map[it->first];
    
    // clears map
    this->data_map.clear();
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
    this->clear_task_sequence();
    this->clear_processes();
    
    if (this->opt != NULL)
    {
        delete this->opt;
        this->opt = NULL;
    }
}

int PyGURLSWrapper::run(char* in_data, char* out_data, char* job_id)
{
    try
    {        
        this->G.run(*(this->data_map[in_data]),*(this->data_map[out_data]),*(this->opt), job_id);
        return EXIT_SUCCESS;
    }
    catch(gException& e)
    {
        cout << e.getMessage() << endl;
        return EXIT_FAILURE;
    }
}

//int PyGURLSWrapper::helloWorld()
//{
//    typedef double T;
//    
//    gMat2D<T> Xtr, Xte, ytr, yte;
//
//    std::string XtrFileName = "Xtr.txt";
//    std::string ytrFileName = "ytr_onecolumn.txt";
//    std::string XteFileName = "Xte.txt";
//    std::string yteFileName = "yte_onecolumn.txt";
//
//    try
//    {
//        //load the training data
//        Xtr.readCSV(XtrFileName);
//        ytr.readCSV(ytrFileName);
//
//        //load the test data
//        Xte.readCSV(XteFileName);
//        yte.readCSV(yteFileName);
//
//
//        //train the classifer
//        GurlsOptionsList* opt = gurls_train(Xtr, ytr);
//
//        //predict the labels for the test set and asses prediction accuracy
//        gurls_test(Xte, yte, *opt);
//
//
//        const gMat2D<T>& acc = opt->getOptValue<OptMatrix<gMat2D<T> > >("acc");
//        const int max = static_cast<int>(*std::max_element(ytr.getData(), ytr.getData()+ytr.getSize()));
//        const int accs = acc.getSize();
//
//        std::cout.precision(4);
//
//        std::cout << std::endl << "Prediction accurcay is:" << std::endl;
//
//        for(int i=1; i<= max; ++i)
//            std::cout << "\tClass " << i << "\t";
//
//        std::cout << std::endl;
//
//        for(int i=0; i< accs; ++i)
//            std::cout << "\t" << acc.getData()[i]*100.0 << "%\t";
//
//        std::cout << std::endl;       
//    }
//    catch (gException& e)
//    {
//        std::cout << e.getMessage() << std::endl;        
//        return EXIT_FAILURE;
//    }
//    
//    return EXIT_SUCCESS;
//}

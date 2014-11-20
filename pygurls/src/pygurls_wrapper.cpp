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
    std::cout << "\tPyGURLSWrapper instance created\n";
}

void PyGURLSWrapper::helloWorld()
{
    typedef double T;
    
    gMat2D<T> Xtr, Xte, ytr, yte;

    std::string XtrFileName = "Xtr.txt";
    std::string ytrFileName = "ytr_onecolumn.txt";
    std::string XteFileName = "Xte.txt";
    std::string yteFileName = "yte_onecolumn.txt";

    try
    {
        //load the training data
        Xtr.readCSV(XtrFileName);
        ytr.readCSV(ytrFileName);

        //load the test data
        Xte.readCSV(XteFileName);
        yte.readCSV(yteFileName);


        //train the classifer
        GurlsOptionsList* opt = gurls_train(Xtr, ytr);

        //predict the labels for the test set and asses prediction accuracy
        gurls_test(Xte, yte, *opt);


        const gMat2D<T>& acc = opt->getOptValue<OptMatrix<gMat2D<T> > >("acc");
        const int max = static_cast<int>(*std::max_element(ytr.getData(), ytr.getData()+ytr.getSize()));
        const int accs = acc.getSize();

        std::cout.precision(4);

        std::cout << std::endl << "Prediction accurcay is:" << std::endl;

        for(int i=1; i<= max; ++i)
            std::cout << "\tClass " << i << "\t";

        std::cout << std::endl;

        for(int i=0; i< accs; ++i)
            std::cout << "\t" << acc.getData()[i]*100.0 << "%\t";

        std::cout << std::endl;       
    }
    catch (gException& e)
    {
        std::cout << e.getMessage() << std::endl;        
    }
}

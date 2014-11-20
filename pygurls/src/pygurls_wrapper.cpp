#include "pygurls_wrapper.h"

using namespace std;
using namespace gurls;

PyGURLSWrapper::PyGURLSWrapper()
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

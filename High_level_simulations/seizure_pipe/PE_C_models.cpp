// PE_models.cpp
extern "C" {
    /*
        * Predicts the output of the SVM model given the model and the input values.
        * @param model The SVM model.
        * @param values The input values.
        * @param size The size of the input values.
        * @return The predicted output.
        

        this will likely take in input vectors from FFT, BBF, and XCORR
        of sizes 96, 96, 120 respectively

        which means the model will be of size 96+96+120 = 312, although I am not too sure as paper says up to 5k
        and inputs (at least for seizure pipe) will be of size 312
    */
    double svm_predict(double* model, unsigned short* values, unsigned short size) {
        double sum = 0;
        for (unsigned short i = 0; i < size; i++) {
            sum += model[i] * values[i];
        }
        return sum;
    }

    
}

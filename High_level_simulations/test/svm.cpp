// svm.cpp
extern "C" {
    double svm_predict(double* model, unsigned short* values, unsigned short size) {
        double sum = 0;
        for (unsigned short i = 0; i < size; i++) {
            sum += model[i] * values[i];
        }
        return sum;
    }
}

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>


extern "C" {
    /*
        * Predicts the output of the SVM model given the model and the input values.
        * @param model The SVM model.
        * @param inputs The input values.
        * @param size The size of the input values.
        * @return The predicted output.
    */
    double svm_predict(double* model, uint16_t* inputs, uint16_t size) {
        double sum = 0;
        for (uint16_t i = 0; i < size; i++) {
            sum += model[i] * inputs[i];
        }
        return sum;
    }

    /*
        * Performs pairwise cross correlation on a predefined number of channels
        * @param inputs 2D array containing samples for num_channels * num_samples 
        * @param num_channels Number of channels.
        * @param num_samples Number of samples per channel.
        * @return All pairwise correlation values
    */
    uint32_t* xcorr(uint16_t* inputs, uint16_t num_channels, uint16_t num_samples) {
        uint16_t num_correlations = (num_channels * (num_channels - 1)) >> 1; // n choose 2
        uint32_t* correlations = (uint32_t*)malloc(num_correlations * sizeof(uint32_t));

        uint32_t z = 0;
        for (uint16_t i = 0; i < num_channels; i++) {
            for (uint16_t j = i + 1; j < num_channels; j++) {
                //find correlation between (i,j)
                uint32_t corr = 0;
                for (uint16_t k = 0; k < num_samples; k++) {
                    corr += inputs[i * num_samples + k] * inputs[j * num_samples + k];
                }
                //save correlation in array sequentially 
                correlations[z++] = corr;
            }
        }
        return correlations;
    }
}

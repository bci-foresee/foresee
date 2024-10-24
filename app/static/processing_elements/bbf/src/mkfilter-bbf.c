#include <stdint.h>
#include <stdio.h>

//this seems to work.

static float filterloop(uint16_t next_input_value, float* xv, float* yv, float* filter_vals, double gain)
{ 
    { 
        xv[0] = xv[1];
        xv[1] = xv[2];
        xv[2] = xv[3];
        xv[3] = xv[4];
        xv[4] = xv[5];
        xv[5] = xv[6];
        xv[6] = xv[7];
        xv[7] = xv[8];
        xv[8] = xv[9];
        xv[9] = xv[10];
        xv[10] = next_input_value / gain;
        yv[0] = yv[1];
        yv[1] = yv[2];
        yv[2] = yv[3];
        yv[3] = yv[4];
        yv[4] = yv[5];
        yv[5] = yv[6];
        yv[6] = yv[7];
        yv[7] = yv[8];
        yv[8] = yv[9];
        yv[9] = yv[10];
        yv[10] =   (xv[10] - xv[0]) + 5 * (xv[2] - xv[8]) + 10 * (xv[6] - xv[4])
            + (filter_vals[0] * yv[0]) + (filter_vals[1] * yv[1])
            + (filter_vals[2] * yv[2]) + (filter_vals[3] * yv[3])
            + (filter_vals[4] * yv[4]) + (filter_vals[5] * yv[5])
            + (filter_vals[6] * yv[6]) + (filter_vals[7] * yv[7])
            + (filter_vals[8] * yv[8]) + (filter_vals[9] * yv[9]);
        return yv[10];
    }
}
float butterworth_filter(uint16_t * sample, uint32_t size){

        //safety checks
        if (sample == NULL || size == 0) {
            return 0;
        }

        //#define NZEROS 10
        //#define NPOLES 10
        static float xv[10+1] = {0}, yv[10+1] = {0};

        // initial test filter values, from the halo github 
        static float filter_vals[] = {-0.0723156691, 0.6368872577, 
                                      -2.8198218361, 8.0640603736,
                                      -16.3818055300, 24.6025699180,
                                      -27.6694600560, 23.0616757780,
                                      -13.6958889160, 5.2541969233};

        //test initial gain 
        static double gain = 3.049509079e+02;
        
        float sum = 0;
        for(uint32_t i = 0 ; i < size ; i++){
            float temp = filterloop(sample[i], 
                                    xv, 
                                    yv,
                                    filter_vals,
                                    gain);
            sum += temp * temp;
        }
        return sum;
    }


int main()
{
    uint16_t sample[1024] = {0}; // Example initialization, ensure it has enough elements
    uint32_t size = 1024;
    float result = butterworth_filter(sample, size);
    printf("Result: %f\n", result);
    return 0;
}

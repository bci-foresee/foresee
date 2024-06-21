#include <verilated.h>
#include "Vexample_top.h"

struct DataPair {
    int* real_output;
    int* imag_output;
};

void setInputs(Vexample_top *pipeline, int real_input, int imag_input) {
    //here we set the inputs to the model
    pipeline->fft_input_real_0 = real_input;
    pipeline->fft_input_real_1 = real_input;
    pipeline->fft_input_real_2 = real_input;
    pipeline->fft_input_real_3 = real_input;

    pipeline->fft_input_imag_0 = imag_input;
    pipeline->fft_input_imag_1 = imag_input;
    pipeline->fft_input_imag_2 = imag_input;
    pipeline->fft_input_imag_3 = imag_input;

}

DataPair collectData(Vexample_top *pipeline) {
    //here we collect data after the next_out signal has been asserted high

    DataPair data_out;

    // 4 outputs per cycle for 256 cycles
    data_out.real_output = new int[4 * 256];
    data_out.imag_output = new int[4 * 256];

    int cycles = 256;

    for (int i = 0; i < cycles*2; i++) {

        int cycle = i/2;

        if (i % 2 == 0) {
            data_out.real_output[cycle*4] = pipeline->fft_output_real_0;
            data_out.real_output[cycle*4 + 1] = pipeline->fft_output_real_1;
            data_out.real_output[cycle*4 + 2] = pipeline->fft_output_real_2;
            data_out.real_output[cycle*4 + 3] = pipeline->fft_output_real_3;

            data_out.imag_output[cycle*4] = pipeline->fft_output_imag_0;
            data_out.imag_output[cycle*4 + 1] = pipeline->fft_output_imag_1;
            data_out.imag_output[cycle*4 + 2] = pipeline->fft_output_imag_2;
            data_out.imag_output[cycle*4 + 3] = pipeline->fft_output_imag_3;
        }

        // Toggle clock
        pipeline->fft_clk = !pipeline->fft_clk;

        // Evaluate the model
        pipeline->eval();
    }

    return data_out;
}

int main(int argc, char **argv, char **env) {
    Verilated::commandArgs(argc, argv);

    Vexample_top *pipeline = new Vexample_top;

    // Initialize simulation inputs

    pipeline->fft_clk = 0;
    pipeline->fft_reset = 0;
    pipeline->fft_next_in = 0;

    int fft_input_real = 100;
    int fft_input_imag = 0;

    setInputs(pipeline, fft_input_real, fft_input_imag);
    
    /*
    input fft_clk,
    input fft_reset,
    input fft_next_in, //asserted high is used to tell the system that the next input will appear on the following cycle

    output fft_next_out, //output will start streaming out the cycle following this asserted high

    input[31:0] fft_input_real_0, // imaginary and real parts of inputs for fft
    input[31:0] fft_input_real_1,
    input[31:0] fft_input_real_2,
    input[31:0] fft_input_real_3,

    input[31:0] fft_input_imag_0,
    input[31:0] fft_input_imag_1,
    input[31:0] fft_input_imag_2,
    input[31:0] fft_input_imag_3,

    output[31:0] fft_output_real_0, // imaginary and real parts of outputs for fft
    output[31:0] fft_output_real_1,
    output[31:0] fft_output_real_2,
    output[31:0] fft_output_real_3,

    output[31:0] fft_output_imag_0,
    output[31:0] fft_output_imag_1,
    output[31:0] fft_output_imag_2,
    output[31:0] fft_output_imag_3
    */

    // Simulate for 20 clock edges
    // therefore it is 10 cycles

    int sim_cycles = 1000;

    // *2 because we are toggling the clock


    for (int i = 0; i < sim_cycles*2; i++) {
        //check for an output
        if (pipeline->fft_next_out) {
            // start collecting data next cycle
            pipeline->eval();
            DataPair collected_data = collectData(pipeline);

            // print data
            for (int i = 0; i < 4*256; i++) {
                printf("Num: %d, Real: %d, Imag: %d\n", i, collected_data.real_output[i], collected_data.imag_output[i]);
            }
        }

        // Reset until cycle 5
        if (i < 5*2) {
            pipeline->fft_reset = 1;
        } else {
            pipeline->fft_reset = 0;
        }

        // start input on cycle 10
        if (i == 10*2) {
            pipeline->fft_next_in = 1;
        } else {
            pipeline->fft_next_in = 0;
        }

        // Toggle clock
        pipeline->fft_clk = !pipeline->fft_clk;

        //on falling edge change values, let computations happen on rising edge
        if (pipeline->fft_clk == 0) {
            // this means it went from high to low = falling edge
            // set inputs
            setInputs(pipeline, fft_input_real, fft_input_imag);
        }


        // Evaluate the model
        pipeline->eval();

        // Print the output
    }

    // top->final();
    pipeline->final();
    delete pipeline;
    return 0;
}

#include <verilated.h>
#include "Vexample_top.h"

int main(int argc, char **argv, char **env) {
    Verilated::commandArgs(argc, argv);

    Vexample_top *pipeline = new Vexample_top;

    // Initialize simulation inputs

    // input clk_adder,
    // input[15:0] adder_op_a,
    // input[15:0] adder_op_b,
    // output[15:0] adder_sum

    pipeline->clk_adder = 0;
    pipeline->adder_op_a = 0;
    pipeline->adder_op_b = 1;


    // Simulate for 20 clock edges
    // therefore it is 10 cycles
    for (int i = 0; i < 20; i++) {
        // Toggle clock
        pipeline->clk_adder = !pipeline->clk_adder;

        //increase op_a if i is even
        if (i % 2 == 0) {
            pipeline->adder_op_a = pipeline->adder_op_a + 2;
        }

        // Evaluate the model
        pipeline->eval();

        // Print the output
        printf("Cycle %d: adder_op_a = %d, adder_op_b = %d, adder_sum = %d\n", i/2, pipeline->adder_op_a, pipeline->adder_op_b, pipeline->adder_sum);
    }

    // top->final();
    pipeline->final();
    delete pipeline;
    return 0;
}

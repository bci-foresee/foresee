#include "Vcounter.h"
#include "Vbit_check.h"
#include "verilated.h"

int main(int argc, char **argv) {
    Verilated::commandArgs(argc, argv);
    
    // Instantiate the modules
    Vcounter* counter = new Vcounter;
    Vbit_check* bit_check = new Vbit_check;

    // Initialize simulation inputs
    counter->clk = 0;
    counter->rst = 1;
    bit_check->in = 0;

    // Simulation time
    int sim_time = 1000;

    for (int i = 0; i < sim_time; i++) {
        // Toggle clock
        counter->clk = !counter->clk;

        // Apply reset for the first two cycles
        if (i < 2) counter->rst = 1;
        else counter->rst = 0;

        // Evaluate the counter
        counter->eval();

        // Pass the counter output to the bit_check input
        bit_check->in = counter->out;

        // Evaluate the bit_check
        bit_check->eval();

        // Print outputs
        printf("Cycle %d: counter_out = %d, bit_check_out = %d\n", i, counter->out, bit_check->out);
    }

    delete counter;
    delete bit_check;
    return 0;
}

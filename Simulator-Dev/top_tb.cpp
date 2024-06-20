#include <verilated.h>
#include "Vtop.h"

int main(int argc, char **argv, char **env) {
    Verilated::commandArgs(argc, argv);

    Vtop *top = new Vtop;

    // Initialize simulation inputs
    top->clk = 0;
    top->reset = 1;

    // Simulate for 20 clock edges
    // therefore it is 10 cycles
    for (int i = 0; i < 20; i++) {
        // Toggle clock
        top->clk = !top->clk;

        // Deassert reset after 2 cycles
        if (i == 2) {
            top->reset = 0;
        }

        // Evaluate the model
        top->eval();

        // Print the output
        printf("Cycle %d: count = %d, bit_check = %d\n", i/2, top->count, top->bit_check);
    }

    top->final();
    delete top;
    return 0;
}

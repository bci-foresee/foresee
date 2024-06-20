#include "Vcounter.h"
#include "verilated.h"

int main(int argc, char **argv) {
    Verilated::commandArgs(argc, argv);
    Vcounter* top = new Vcounter;

    //init inputs
    top->clk = 0;
    top->rst = 0;
    
    //what clock cycle to go to
    int sim_time = 100;

    for (int i = 0; i < sim_time; i++) {
        //toggle clk
        top->clk = !top->clk;
        
        //reset for first two cycles
        if (i < 2) top->rst = 1;
        else top->rst = 0;

        //eval (run the module)
        top->eval();

        //print output
        printf("Cycle %d: out = %d\n", i, top->out);

        //the top->"names" are all derived from the module in v file.
        // i think we can just import several of these modules.
    }

    delete top;
    return 0;
}

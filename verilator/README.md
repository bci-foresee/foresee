# Verilator

The idea is to elevate our Verilog implementations directly into C code.

TODO: Unsure if this directory will remain. Decide later.

## Old Notes

If additional control is needed, you can code up testbenches using Verilator and C. An example of this is within the [Verilator-C-Simulator](./Verilator-C-Simulator) folder.

To use this, you need to create a top level module like [example_top.v](./Verilator-C-Simulator/Verilog-APaths/example_top.v) and then create a testbench in C like [example_tb.cpp](./Verilator-C-Simulator/example_tb.cpp). The example shows how to test the FFT (although there is no post processing analysis there, it should be easy to add).

Then to run the simulation you can run the following in the terminal. 

*Make sure to have verilator installed, this was tested on an apple silicon mac, and github codespaces (which is a Linux environment).*

```sh
#inside Verilator-C-Simulator

#compilation of the verilog
verilator -cc ./Verilog-APaths/example_top.v ./Verilog-PEs/spiral-fft.v --exe example_tb.cpp

#go to verilated files directory
cd obj_dir

#make the verilated files, only need to redo this if changing just the testbench (example_tb.cpp)
make -f Vexample_top.mk

#run the simulation
./Vexample_top

```
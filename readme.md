# HALO/SCALO simulator

**Table of contents**
- [Overview](#overview)
- [Python Simulator](#python-simulator)
- [C Simulator](#c-verilator-simulator)

## Overview
This is some software developed to help simulate the HALO/SCALO architecture. 

Why? To allow for modular testing of the architecture which in turn should allow for rapid idea testing and development. 

Furthermore, this should allow for quicker ideation -> simulation -> testing -> tapeout cycles.

The general idea is to have verilog modules created that can be plugged in like lego, and then tested from a high level Python environment that lets you test out many things such as clock speeds, FIFO sizes, etc. Also, the Python environment allows for "ideal" functions to be created to test your verilog, ie I could test my FFT simply by doing an `assert FFT_out == np.FFT(data)` or something similar.

## Python Simulator

The Python simulation is made because the [C/Verilator simulator](#c-verilator-simulator) is too low level to allow for rapid development and Python has many more useful tools at its disposal.

The simulator is build with [cocotb](https://www.cocotb.org), and the development has mostly been done in a GitHub Codespaces environment (which is Linux based). In theory this should work with any x86 system.

An example showing the FFT module being tested is in [test_FFT.py](./SCALO_sim/FFT_test/test_FFT.py). 

The rest is currently under development.

## C (Verilator) Simulator

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
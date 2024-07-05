# HALO/SCALO simulator

## Introduction
This is some software developed to help simulate the HALO/SCALO architecture. 

Why? To allow for modular testing of the architecture which in turn should allow for rapid idea testing and development. 

Furthermore, this should allow for quicker ideation -> simulation -> testing -> tapeout cycles.

The general idea is to make it as easy as possible to test different pipelines with minimal effort, in whichever language you want (Verilog, C or Python). This can allow for rapid ideation with Python/C and then a more detailed, hardware accurate simulation with Verilog.

## Table of contents
- [Introduction](#introduction)
- [Simulator Overview](#simulator-overview)
- [Environment Setup](#environment-setup)
- ... to do

## Simulator Overview

The most up to date version of the Simulator can be seen in [./Combined_Simulator/shiao](./Combined_Simulator/shiao). This is an example pipeline that demonstrates what the simulator does and its structure with the seizure detection pipeline for the SCALO architecture.

This tree below shows the important components of the simulator, although this tree is non-exhaustive. Each file/subdirectory here is related to a section of this document that explains what it does. This document is still a work in progress and will be updated as the simulator is developed.

```
.
└── [shiao](./Combined_Simulator/shiao)
    ├── Makefile
    ├── pipeline.py
    ├── plots
    │   ├── python_PEs
    │   ├── rtl_PEs
    │   └── signal_gen
    ├── processing_elements
    │   ├── c_PEs
    │   ├── python_PEs
    │   ├── rtl_PEs
    │   ├── rtl_toplevel
    │   └── rtl_wrappers
    ├── dev_tests
    └── signal_gen
        ├── simple_signal_gen.py
        └── ...
```

## Environment Setup

The simulator was developed in a GitHub Codespaces environment, which is a Linux based environment. The device information is shown below.

`Linux codespaces 6.5.0-1022-azure #23~22.04.1-Ubuntu SMP x86_64 x86_64 x86_64 GNU/Linux`

Furthermore, the simulator uses Python 3.10.14 as its interface. There are a few dependencies that need to be installed to run the simulator. The dependencies are in the [environment.yml](./environment.yml) file. You can easily create and activate an identical conda environment by running the following command. This should get you set up.

```sh
conda env create -f environment.yml
conda activate scalo_sim
```

Then you can run the example shiao pipeline by first going to the [shiao](./Combined_Simulator/shiao) directory and running the following command.

```sh
make
```

### Makefile

The makefile should include the following components. It's used by cocotb to define the simulation environment.

```makefile
TOPLEVEL_LANG = verilog
```

```makefile
VERILOG_SOURCES = $(shell pwd)/processing_elements/rtl_toplevel/seizure_pipe.v
VERILOG_SOURCES += $(shell pwd)/processing_elements/rtl_PEs/spiral_fft_8192.v
TOPLEVEL = seizure_pipe
MODULE = pipeline
include $(shell cocotb-config --makefiles)/Makefile.sim
```

# --- old docs ---

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

# Notes

- make sure to add dependencies in some way
    - they are in codespaces, conda environment verilog_env
# ALOHA

![PE Tests](https://github.com/ysarch-lab/aloha-verilog/actions/workflows/test-suite.yml/badge.svg)


This is a development platform for designing, testing, and validating chips for neural interfaces.
It is heavily inspired by the HALO/SCALO design methodology which, at its core, provides a modular accelerator framework.

The general idea is to make it as easy as possible to test different pipelines with minimal effort, in whichever language you want (Verilog, C or Python). This can allow for rapid ideation with Python/C and then a more detailed, hardware accurate simulation with Verilog. The Verilog simulator is built with [cocotb](https://www.cocotb.org).

## TODOs
- Add `pydoc`
- Enforce `mypy`
- Add automatic formatting of Python style

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
conda env create -f environment.yaml
conda activate scalo_sim
```

Then you can run the example shiao pipeline by first going to the [shiao](./Combined_Simulator/shiao) directory and running the following command.

```sh
make
```

*note: to remove a conda environment, use `conda env remove --name your_env_name`*


*unfinished section*

### SSH grace getting resources:

```sh
# getting an interactive session
srun --ntasks=1 --cpus-per-task=4 --mem=64GB --time=01:00:00 --partition=scavenge --pty bash

# figuring out host of resources
hostname

# ssh to hostname to get those resources ie r911u01n02.grace.ycrc.yale.edu
ssh [hostname]

# exit when done
exit
```

### Makefile

The makefile should include the following components. It's used by cocotb to define the simulation environment.


```makefile
TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(shell pwd)/processing_elements/rtl_toplevel/seizure_pipe.v
VERILOG_SOURCES += $(shell pwd)/processing_elements/rtl_PEs/spiral_fft_8192.v
TOPLEVEL = seizure_pipe
MODULE = pipeline
include $(shell cocotb-config --makefiles)/Makefile.sim
```
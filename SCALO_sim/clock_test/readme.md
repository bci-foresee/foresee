https://docs.cocotb.org/en/stable/quickstart.html

Ensure you are in the verilog_env conda environment.

```sh
conda activate verilog_env
```

look at `from cocotb.clock import Clock`, could be useful for clock gen.


In order to run a test, you create a Makefile that contains information about your project (i.e. the specific DUT and test).

In the Makefile shown below we specify:

the default simulator to use (SIM),
the default language of the toplevel module or entity (TOPLEVEL_LANG, verilog in our case),
the design source files (VERILOG_SOURCES and VHDL_SOURCES),
the toplevel module or entity to instantiate (TOPLEVEL, my_design in our case),
and a Python module that contains our cocotb tests (MODULE. The file containing the test without the .py extension, test_my_design in our case).

to run: 
```sh
make
```

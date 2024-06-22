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

## other useful ideas

multi clock gen:
```python
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

@cocotb.test()
async def test_multi_clock_design(dut):
    # Create a 15.7 MHz clock on clk_a (approx. 63.69 ns period)
    clock_a = Clock(dut.clk_a, 63.69, units="ns")
    
    # Create a 10 MHz clock on clk_b (100 ns period)
    clock_b = Clock(dut.clk_b, 100, units="ns")
    
    # Start both clocks
    cocotb.start_soon(clock_a.start())
    cocotb.start_soon(clock_b.start())

    # Wait for initial setup
    await Timer(1, units="us")

    # Testing logic
    for _ in range(100):
        await RisingEdge(dut.clk_a)  # Wait for a rising edge of clk_a
        # Perform operations related to clk_a

    for _ in range(100):
        await RisingEdge(dut.clk_b)  # Wait for a rising edge of clk_b
        # Perform operations related to clk_b

    # Additional synchronization and testing logic for multi-clock interaction
    for _ in range(100):
        await RisingEdge(dut.clk_a)
        await RisingEdge(dut.clk_b)
        # Perform operations that depend on both clocks

    # Optionally, add checks or assertions to verify correct behavior
```


^C during sim allows debug mode:
```sh
Commands can be from the following table of base commands,
or can be invocations of system tasks/functions.

cd       - Synonym for push.
cont     - Resume (continue) the simulation
finish   - Finish the simulation.
help     - Get help.
list     - List items in the current scope.
load     - Load a VPI module, a la vvp -m.
ls       - Shorthand for "list".
pop      - Pop one scope from the scope stack.
push     - Descend into the named scope.
step     - Single-step the scheduler for 1 event.
time     - Print the current simulation time.
trace    - Control statement tracing (on/off) when the code is instrumented.
where    - Show current scope, and scope hierarchy stack.

If the command name starts with a '$' character, it
is taken to be the name of a system task, and a call is
built up and executed.
```

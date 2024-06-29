python notes for multi module testing:
```python
import cocotb
from cocotb.triggers import Timer

async def adder_verilog(dut, a, b):
    # Apply inputs to the adder
    dut.a <= a
    dut.b <= b

    # Wait for a small amount of time to simulate the propagation delay
    await Timer(1, units='ns')

    # Get the output from the adder
    sum_result = dut.sum.value.integer

    return sum_result

async def subtractor_verilog(dut, c, d):
    # Apply inputs to the subtractor
    dut.c <= c
    dut.d <= d

    # Wait for a small amount of time to simulate the propagation delay
    await Timer(1, units='ns')

    # Get the output from the subtractor
    sub_result = dut.sub.value.integer

    return sub_result

@cocotb.test()
async def test_adder_only(dut):
    # Test cases for the adder
    test_cases = [
        (0, 0, 0),
        (1, 1, 2),
        (2, 3, 5),
        (4, 7, 11),
        (8, 8, 16),
        (15, 15, 30)
    ]

    for a, b, expected in test_cases:
        result = await adder_verilog(dut, a, b)
        assert result == expected, f"Adder failed for {a} + {b}, expected {expected}, got {result}"
        cocotb.log.info(f"Adder test passed for {a} + {b} = {result}")

@cocotb.test()
async def test_subtractor_only(dut):
    # Test cases for the subtractor
    test_cases = [
        (0, 0, 0),
        (1, 1, 0),
        (3, 2, 1),
        (7, 4, 3),
        (8, 8, 0),
        (15, 10, 5)
    ]

    for c, d, expected in test_cases:
        result = await subtractor_verilog(dut, c, d)
        assert result == expected, f"Subtractor failed for {c} - {d}, expected {expected}, got {result}"
        cocotb.log.info(f"Subtractor test passed for {c} - {d} = {result}")

@cocotb.test()
async def test_adder_and_subtractor(dut):
    # Use the output of the adder as input to the subtractor
    a, b, d = 3, 5, 4
    sum_result = await adder_verilog(dut, a, b)
    sub_result = await subtractor_verilog(dut, sum_result, d)
    expected_sub_result = sum_result - d
    assert sub_result == expected_sub_result, f"Subtractor failed for {sum_result} - {d}, expected {expected_sub_result}, got {sub_result}"
    cocotb.log.info(f"Subtractor test passed for {sum_result} - {d} = {sub_result}")
```

old makefile:
```makefile
# Makefile

TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(shell pwd)/verilog_PEs/seizure_pipe.v
VERILOG_SOURCES += $(shell pwd)/verilog_PEs/spiral_fft.v
TOPLEVEL = seizure_pipe
MODULE = test_FFT

include $(shell cocotb-config --makefiles)/Makefile.sim
```
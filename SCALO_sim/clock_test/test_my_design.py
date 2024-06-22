# test_my_design.py (simple)

import cocotb
from cocotb.triggers import Timer


# this marks the function as a test
@cocotb.test()
async def my_first_test(dut):
    """Try accessing the design."""

    for cycle in range(10):
        dut.clk.value = 0 # assigning a value to the signal
        await Timer(1, units="ns")
        dut.clk.value = 1
        await Timer(1, units="ns") # suspends the test until the function is evaluated

    # dut.thingy.value is how to get the value of the signal in "thingy"
    dut._log.info("my_signal_1 is %s", dut.my_signal_1.value)
    assert dut.my_signal_2.value[0] == 0, "my_signal_2[0] is not 0!"
"""
This file defines the base class for all hardware components
"""
# TODO(btrevisan): create a function that gives the detailed information for the pe and allow for edits
# TODO(btrevisan): reorganize the app and directories. keep command linge stuff
import subprocess
import re
import numpy as np
import struct
import os
from numpy.typing import NDArray


class ProcessingElement:

    def __init__(self,
                 name: str,
                 clk: int = 0,
                 rtl_sim: bool = False,
                 rtl_power_estimation: bool = False,
                 save_visualization: bool = False) -> None:

        # name of the processing element
        self.name = name

        # clock frequency
        #  TODO btrevisan : add to the plot
        self.clk = clk

        # False means run python implementation, True means run verilog implementation
        self.rtl_sim = rtl_sim

        if rtl_power_estimation:
            if clk == 0:
                raise ValueError(
                    "Please provide a clock frequency (PE.clk, in Hz) for the RTL simulation"
                )
            else:
                self.clk = clk

        # False means do not run power estimation, True means run power estimation
        self.rtl_power_estimation = rtl_power_estimation

        # save vizualisation of processing element
        self.save_visualization = save_visualization

        # i/o
        self.inputs = []
        self.outputs = []

        # name the input and output buffers - used for the verilog simulation
        self.input_buffer = "input_buffer.txt"
        self.output_buffer = "output_buffer.txt"

    def get_tooltip(self):
        tooltip_text = f"{self.name}\n"
        tooltip_text += f"Clock Frequency: {self.clk}\n"
        tooltip_text += f"Run Power Estimation: {self.rtl_power_estimation}\n"
        tooltip_text += f"RTL Simulation: {self.rtl_sim}"
        return tooltip_text

    # add inputs to the processing element
    def add_input(self, node: 'ProcessingElement') -> None:
        if node not in self.inputs:
            self.inputs.append(node)

    # add outputs from the processing element
    def add_output(self, node: 'ProcessingElement') -> None:
        if node not in self.outputs:
            self.outputs.append(node)

    # to run the PE's verilog implementation
    def run_verilog_simulation(self, PE_name, verilog_file, output_file):
        # Run the Verilog simulation using Icarus Verilog or another Verilog simulator
        # Get the top-level directory of the Git repo
        # top_level_dir = subprocess.run(["git", "rev-parse", "--show-toplevel"],
        #                                capture_output=True,
        #                                text=True).stdout.strip()

        # # Change the directory in Python
        # os.chdir(f"{top_level_dir}/asa/{PE_name.lower()}")
        subprocess.run([
            "iverilog", "-o", f"./rtl/{verilog_file}_sim.vvp",
            f"./rtl/{verilog_file}_tb.v", f"./rtl/{verilog_file}.v"
        ])
        subprocess.run(["vvp", f"./rtl/{verilog_file}_sim.vvp"])

        # tests
        if self.rtl_power_estimation:
            power_estimate = self.run_rtl_power_estimation(
                verilog_file=verilog_file,
                process_library=
                "../../hardware_lib/sky130_fd_sc_hd__ff_n40C_1v65",
                clock_freq=self.clk)
            for key, value in power_estimate.items():
                print(f"{key}:")
                for k, v in value.items():
                    print(f"  {k}: {v}")

        # Read the output
        numbers = []
        with open(output_file, 'r') as file:
            for line in file:
                # Split each line into words and convert each word from hex to int
                line_numbers = [int(word, base=16) for word in line.split()]
                numbers.extend(line_numbers)

        # Convert the list of numbers to a numpy array
        return np.array(numbers)

    # to run the PE's rtl power estimation
    def run_rtl_power_estimation(self, verilog_file, process_library,
                                 clock_freq):

        clock_period_ns = (1 / clock_freq) * 1e9

        # Create Yosys synthesis script
        self.create_yosys_synth_file(verilog_file=verilog_file,
                                     process_library=process_library)

        # Create OpenSTA power analysis script
        self.create_power_opesta_tcl_file(verilog_file=verilog_file,
                                          process_library=process_library,
                                          clock_period=clock_period_ns)

        # Run Yosys
        yosys_cmd = "yosys -s synth.ys"
        subprocess.run(yosys_cmd, shell=True, check=True, timeout=None)

        # Run OpenSTA
        opensta_cmd = "../../external/OpenSTA/app/sta power_analysis.tcl"
        result = subprocess.run(opensta_cmd,
                                shell=True,
                                check=True,
                                capture_output=True,
                                text=True,
                                timeout=None)

        # Pattern to match each row of the power data
        pattern = re.compile(
            r"(\w+)\s+([\d.e+-]+)\s+([\d.e+-]+)\s+([\d.e+-]+)\s+([\d.e+-]+)\s+([\d.e+-]+)%?"
        )

        # Dictionary to store power data
        power_data = {}

        # Find all matches and store them in the dictionary
        for match in pattern.findall(result.stdout):
            group_name = match[0]
            internal_power = float(match[1])
            switching_power = float(match[2])
            leakage_power = float(match[3])
            total_power = float(match[4])
            percentage = float(match[5])

            # Store each entry in a nested dictionary
            power_data[group_name] = {
                'Internal Power': internal_power,
                'Switching Power': switching_power,
                'Leakage Power': leakage_power,
                'Total Power': total_power,
                'Percentage': percentage
            }

        return power_data

    # necessary method to run the processing element
    def run(self) -> NDArray[np.float32]:
        # Get the top-level directory of the Git repo
        top_level_dir = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                                       capture_output=True,
                                       text=True).stdout.strip()

        # Change the directory in Python
        os.chdir(f"{top_level_dir}/asa/{self.name.lower()}")

        # load input data
        input_data = self.load_inputs()
        # validate dimensions
        self.dimension_validate(input=input_data)
        # compute
        if self.rtl_sim:
            output = self.compute_verilog(
                input=input_data)  # replace with verilog compute
        else:
            output = self.compute(input=input_data)

        # vizualise
        if self.save_visualization:
            self.visualize()
        # return data
        return output

    def int_to_signedHex(self, value: int) -> str:
        item = f"{struct.unpack('I', struct.pack('i', value))[0]:08x}"
        return item

    # necessary method to load input data from input processing elements
    def load_inputs(self):
        raise NotImplementedError("run method not implemented")

    # necessary method to validate the dimensions of the input data
    def dimension_validate(self):
        raise NotImplementedError("run method not implemented")

    # necessary method to calculate processing egraphviz -Vlement's computation
    def compute(self):
        raise NotImplementedError("run method not implemented")

    # method to compute using the verilog implementation of PE
    def compute_verilog(self):
        raise NotImplementedError("run method not implemented")

    # necessary method to validate the dimensions of the input data
    def visualize(self, graph):
        return graph.add_node(self.name)

    def create_yosys_synth_file(self, verilog_file, process_library):
        # function that creates a yosys synthesis script
        # used for PE power estimation

        # ie process_library = "sky130_fd_sc_hd__ff_n40C_1v65.lib"
        # verilog_file = "clocked_adder.v"

        content = f"""
        # Read the Verilog file
        read_verilog ./rtl/{verilog_file}.v

        # Perform synthesis with a generic library
        synth -top {verilog_file}

        # Map to standard cells (replace 'mycells.lib' with your library)
        dfflibmap -liberty {process_library}.lib
        abc -liberty {process_library}.lib

        # Write the gate-level netlist to a file
        write_verilog ./rtl/{verilog_file}_synth.v
        """
        with open("synth.ys", "w") as f:
            f.write(content)

    def create_power_opesta_tcl_file(self, verilog_file, process_library,
                                     clock_period):
        # function that creates a power analysis tcl script
        # used for PE power estimation

        incl_switching_activity = False
        switching_activity = 0.2
        comment_sw = "# "
        if incl_switching_activity:
            comment_sw = ""

        debug = False
        comment_db = "# "
        if debug:
            comment_db = ""

        content = f"""
        # Read the synthesized netlist
        read_verilog ./rtl/{verilog_file}_synth.v

        # Read the standard cell library
        read_liberty {process_library}.lib

        # Link the design to resolve references, name of top level module
        link_design {verilog_file}

        # Read the design constraints
        # read_sdc clocked_adder.sdc
        create_clock -period {clock_period} [get_ports clk]

        # Manually estimate switching activity (you may have to estimate this externally)
        # switching activity, 0.2 normal??
        {comment_sw}set_power_activity -input -activity {switching_activity}
        # for example when a certain port will never toggle:
        # set_power_activity -input_port reset -activity 0.0
        read_power_activities -vcd sim.vcd

        # debug statement
        {comment_db}check_setup -verbose

        # Perform a simplified power analysis based on the static power and estimated switching activity
        report_power

        # exit
        exit

        # report_checks
        # report_units
        # could be used to estimate latency?
        # report_checks -path_delay max -group_count 5
        """
        with open("power_analysis.tcl", "w") as f:
            f.write(content)

    # return way to identify the processing element
    def __repr__(self) -> str:
        return f"{self.name}"

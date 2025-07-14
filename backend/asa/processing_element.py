"""
This file defines the base class for all hardware components
"""
# TODO(btrevisan): create a function that gives the detailed information for the pe and allow for edits
# TODO(btrevisan): reorganize the app and directories. keep command linge stuff
"""
This file defines the base class for all hardware components
"""

import subprocess
import re
import numpy as np
import struct
import os
import logging

from numpy.typing import NDArray

logging.basicConfig(filename='backend.log', level=logging.DEBUG)

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
        self.clk = clk

        # False means run python implementation, True means run verilog implementation
        self.rtl_sim = rtl_sim

        if rtl_power_estimation:
            if clk <= 0:
                raise ValueError(
                    "Please provide a clock frequency (PE.clk, in Hz) for the RTL simulation"
                )
            else:
                self.clk = clk

        # False means do not run power estimation, True means run power estimation
        self.rtl_power_estimation = rtl_power_estimation

        # how many times this rtl module was ran.
        # this is important for power estimation
        # ie if we did 16 idential runs of the same module, we can multiply the power by 16
        # this is used for when we have multiple channels in signals
        self.rtl_module_runs = 0

        # for a single run, how many times was module ran
        # this is for example if a module is ran 8192 times for a single signal window
        self.rtl_single_module_runs = 0

        # save vizualisation of processing element
        self.save_visualization = save_visualization

        # i/o
        self.inputs = []
        self.outputs = []

        # name the input and output buffers - used for the verilog simulation
        self.input_buffer = "input_buffer.txt"
        self.output_buffer = "output_buffer.txt"

        self.simulation_data = {
            "name": self.name,
            "simulation_type": None,
            "input_dimensions": None,
            "output_dimensions": None,
            "output_data": None,
            "power_dict": None,
            "clock_frequency": None,
            "latency":
            None  # this can be calculated using clock frequency and latency (in cycles) of the PE
        }

        if self.rtl_sim:
            self.simulation_data["simulation_type"] = "RTL"
            self.simulation_data["clock_frequency"] = self.clk
        else:
            self.simulation_data["simulation_type"] = "Python"

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
        
        # Debug environment info
        import shutil
        logging.info(f"🔧 Verilog simulation debug for {PE_name}:")
        logging.info(f"  Current working directory: {os.getcwd()}")
        logging.info(f"  iverilog location: {shutil.which('iverilog') or 'NOT FOUND'}")
        logging.info(f"  vvp location: {shutil.which('vvp') or 'NOT FOUND'}")
        logging.info(f"  PATH: {os.environ.get('PATH', 'NOT SET')}")
        logging.info(f"  CONDA_DEFAULT_ENV: {os.environ.get('CONDA_DEFAULT_ENV', 'NOT SET')}")
        logging.info(f"  CONDA_PREFIX: {os.environ.get('CONDA_PREFIX', 'NOT SET')}")
        
        try:
            # Compile verilog
            iverilog_cmd = [
                "iverilog", "-o", f"./rtl/{verilog_file}_sim.vvp",
                f"./rtl/{verilog_file}_tb.v", f"./rtl/{verilog_file}.v"
            ]
            logging.info(f"Running iverilog: {' '.join(iverilog_cmd)}")
            
            compile_result = subprocess.run(iverilog_cmd, 
                                          capture_output=True, text=True, check=True)
            logging.info("✅ iverilog compilation successful")
            
            # Check if vvp file was created
            vvp_file = f"./rtl/{verilog_file}_sim.vvp"
            if not os.path.exists(vvp_file):
                raise RuntimeError(f"iverilog did not create expected file: {vvp_file}")
            
            # Run simulation
            vvp_cmd = ["vvp", f"./rtl/{verilog_file}_sim.vvp"]
            logging.info(f"Running vvp: {' '.join(vvp_cmd)}")
            
            sim_result = subprocess.run(vvp_cmd, 
                                       capture_output=True, text=True, check=True)
            logging.info("✅ vvp simulation successful")
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Verilog simulation failed: {e}"
            if e.stdout:
                error_msg += f"\nSTDOUT: {e.stdout}"
            if e.stderr:
                error_msg += f"\nSTDERR: {e.stderr}"
            logging.error(error_msg)
            raise RuntimeError(error_msg + ". This usually means 'iverilog' is not installed or not available in PATH.")
        except Exception as e:
            error_msg = f"Verilog simulation error: {e}"
            logging.error(error_msg)
            raise RuntimeError(error_msg)

        # # tests
        # if self.rtl_power_estimation:
        #     power_estimate = self.run_rtl_power_estimation(
        #         verilog_file=verilog_file,
        #         process_library=
        #         "../../hardware_lib/sky130_fd_sc_hd__ff_n40C_1v65",
        #         clock_freq=self.clk)
        #    for key, value in power_estimate.items():
        #        print(f"{key}:")
        #        for k, v in value.items():
        #            print(f"  {k}: {v}")

        # Read the output
        numbers = []
        with open(output_file, 'r') as file:
            for line in file:
                # Split each line into words and convert each word from hex to int
                line_numbers = [int(word, base=16) for word in line.split()]
                numbers.extend(line_numbers)

        self.rtl_module_runs += 1  # how many times this rtl module was run. We don't need to power estimate more than once

        # Convert the list of numbers to a numpy array
        return np.array(numbers)

    # to run the PE's rtl power estimation
    def run_rtl_power_estimation(self, verilog_file, process_library,
                                 clock_freq):

        clock_period_ns = (1 / clock_freq) * 1e9

        # Create Yosys synthesis script
        self.create_yosys_synth_file(verilog_file=verilog_file,
                                     process_library=process_library)

        self.create_sdc_constraints(verilog_file, clock_period_ns)

        # Create OpenSTA power analysis script
        self.create_power_opesta_tcl_file(verilog_file=verilog_file,
                                          process_library=process_library,
                                          clock_period=clock_period_ns)

        # Run Yosys
        yosys_cmd = "yosys -s synth.ys"
        subprocess.run(yosys_cmd, shell=True, check=True, timeout=None)

        # Run OpenSTA (optional – skip if tool not available)
        opensta_cmd = "../../external/OpenSTA/build/sta power_analysis.tcl"
        try:
            result = subprocess.run(opensta_cmd,
                                    shell=True,
                                    check=True,
                                    capture_output=True,
                                    text=True,
                                    timeout=None)
            opensta_output = result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            # If OpenSTA is not installed or the command fails, continue without power/latency data.
            opensta_output = ""
            logging.debug(f"OpenSTA command failed: {opensta_cmd}")

        # Pattern to match each row of the power data
        pattern = re.compile(
            r"(\w+)\s+([\d.e+-]+)\s+([\d.e+-]+)\s+([\d.e+-]+)\s+([\d.e+-]+)\s+([\d.e+-]+)%?"
        )

        # Dictionary to store power data
        power_data = {}

        # Find all matches and store them in the dictionary
        for match in pattern.findall(opensta_output):
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

        # Refined regex to target the specific "data arrival time" pattern
        pattern = re.compile(
            r"\s+([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s+data arrival time")

        # Find all matches and extract the data arrival times
        arrival_times = [
            float(match.group(1)) for match in pattern.finditer(opensta_output)
        ]

        if arrival_times:
            self.simulation_data["latency"] = max(arrival_times)

        if 'Total' in power_data:
            self.simulation_data["power_dict"] = power_data['Total']
        else:
            # fallback if power data not available
            self.simulation_data["power_dict"] = {}

        return power_data if power_data else {}

    # necessary method to run the processing element
    def run(self) -> NDArray[np.float32]:
        # Get the project root directory - works both in development and packaged app
        from asa.utils import get_project_root
        
        top_level_dir = get_project_root()

        # Change the directory in Python
        target_dir = os.path.join(top_level_dir, "backend", "asa", self.name.lower())
        if not os.path.exists(target_dir):
            raise RuntimeError(f"Processing element directory not found: {target_dir}")
        
        os.chdir(target_dir)

        # load input data
        input_data = self.load_inputs()

        # store input dimensions for sim_data
        self.simulation_data["input_dimensions"] = np.array(input_data).shape

        # loading inputs changes directory, so reset
        top_level_dir = get_project_root()

        # Change the directory in Python
        target_dir = os.path.join(top_level_dir, "backend", "asa", self.name.lower())
        os.chdir(target_dir)

        # validate dimensions
        self.dimension_validate(input=input_data)
        # compute
        if self.rtl_sim:
            output = self.compute_verilog(
                input=input_data)  # replace with verilog compute

            # run power estimation once, multiply by number of rtl runs

            # power estimation
            if self.rtl_power_estimation:
                power_estimate = self.run_rtl_power_estimation(
                    verilog_file=self.name.lower(),
                    process_library=
                    "../../hardware_lib/sky130_fd_sc_hd__ff_n40C_1v65",
                    clock_freq=self.clk)

                # multiply power by number of rtl runs
                # total power is what is relevant to us right now
                for key, value in self.simulation_data["power_dict"].items():
                    # self.simulation_data["power_dict"][key] = value * self.rtl_module_runs
                    # self.simulation_data["power_dict"]
                    if key != 'Percentage':
                        self.simulation_data["power_dict"][key] = value * self.rtl_module_runs * max(1, self.rtl_single_module_runs)

                # multiply latency by how many times module has to be repeated
                if self.simulation_data["latency"] is not None:
                    self.simulation_data["latency"] *= max(1, self.rtl_single_module_runs)

        else:
            output = self.compute(input=input_data)

        print(
            f"{self.name} input.shape: {np.array(input_data).shape} output.shape: {np.array(output).shape}"
        )

        # store output dimensions for sim_data
        self.simulation_data["output_dimensions"] = np.array(output).shape
        self.simulation_data["output_data"] = output

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

    # necessary method to calculate processing element's computation
    def compute(self):
        raise NotImplementedError("run method not implemented")

    # method to compute using the verilog implementation of PE
    def compute_verilog(self):
        raise NotImplementedError("run method not implemented")

    # necessary method to validate the dimensions of the input data
    def vizualise(self):
        raise NotImplementedError("run method not implemented")

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

    def create_sdc_constraints(self,
                               verilog_file,
                               clock_period,
                               input_delay=2.0,
                               output_delay=1.5):
        """
        Create SDC constraints file for timing analysis
        Args:
            verilog_file: Name of the verilog module/file
            clock_period: Clock period in nanoseconds
            input_delay: Maximum input delay (default 2.0ns)
            output_delay: Maximum output delay (default 1.5ns)
        """
        content = f"""
        # Clock definition
        create_clock -name clk -period {clock_period} [get_ports clk]
        set_clock_uncertainty 0.1 [get_clocks clk]

        # Input delays for all synchronous inputs
        set_input_delay -clock clk -max {input_delay} [all_inputs]
        set_input_delay -clock clk -min {input_delay / 4} [all_inputs]

        # Output delays
        set_output_delay -clock clk -max {output_delay} [all_outputs]
        set_output_delay -clock clk -min {output_delay / 3} [all_outputs]

        # Load capacitance for all outputs
        set_load 0.1 [all_outputs]
        """

        # sdc_path = f"./rtl/{verilog_file}.sdc"
        with open("constraints.sdc", "w") as f:
            f.write(content)
        # print(f"SDC constraints written to {sdc_path}")

        # ... rest of the function

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
        read_sdc constraints.sdc
        create_clock -period {clock_period} [get_ports clk]

        # Manually estimate switching activity (you may have to estimate this externally)
        # switching activity, 0.2 normal
        {comment_sw}set_power_activity -input -activity {switching_activity}
        # for example when a certain port will never toggle:
        # set_power_activity -input_port reset -activity 0.0
        # read_power_activities -vcd sim.vcd

        # debug statement
        {comment_db}check_setup -verbose

        # Perform a simplified power analysis based on the static power and estimated switching activity
        report_power

        # timing analysis
        report_checks -path_delay max -group_count 1

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

import json
import shutil
import subprocess
from enum import Enum
import pandas as pd
from pathlib import Path
from utils import CellType, OpTarget, ResultType
from typing import List

# Example usage:

# model = StorageModel(
#     read_frequency=100000,
#     write_frequency=10,
#     read_size=8,
#     write_size=8,
#     cell_type=CellType.RRAM,
#     process_node=22,
#     opt_target=OpTarget.ReadLatency,
#     word_width=64,
#     capacity=1,
#     bits_per_cell=1,
# )

# model.run()
# model.display_summary()
# model.cleanup()

# NVSimcovers the process nodes from 180 nm, 120 nm, 90 nm, 65nm,45 nm, 32 nm to 22 nm


class StorageModel:
    """
    A class to model storage performance from various workload and cell configurations.
    """

    def __init__(
            self,
            read_frequency: int,
            write_frequency: int,
            read_size: int,
            write_size: int,
            cell_type: CellType,
            word_width: int = 16,
            process_node:
        int = 22,  #TODO: figure out what this does / why it doesn't trigger new output file
            opt_target: OpTarget = OpTarget.ReadLatency,
            capacity: int = 1,
            bits_per_cell: int = 1):
        self.nvm_explorer_path = Path(
            __file__).resolve().parent / "nvmexplorer"
        self.config = {
            "experiment": {
                "read_frequency":
                read_frequency,
                "write_frequency":
                write_frequency,
                "read_size":
                read_size,
                "write_size":
                write_size,
                "cell_type": [cell_type.value],
                "process_node":
                process_node,
                "opt_target": [opt_target.value],
                "word_width":
                word_width,
                "capacity": [capacity],
                "bits_per_cell": [bits_per_cell],
                "nvsim_path":
                str(self.nvm_explorer_path / "nvmexplorer_src" / "nvsim_src" /
                    "nvsim"),
                "output_path":
                str(self.nvm_explorer_path / "output"),
                "custom_cells": True
            },
            "custom_cells": []
        }
        self.config_file_path = self.nvm_explorer_path / "config" / "storage_model.json"
        self.results = None

    def run(self):
        '''Runs model in nvmexplorer.'''
        print("Running model...")
        # check if nvsim executable exists
        nvsim_path = self.nvm_explorer_path / "nvmexplorer_src" / "nvsim_src" / "nvsim"
        if not nvsim_path.exists():
            raise FileNotFoundError(
                f"NVSim executable does not exist. Write 'make' in {nvsim_path.parent()}."
            )

        # save config file in nvmexplorer
        self.save_config()

        # run nvmexplorer
        run_py_path = self.nvm_explorer_path / 'run.py'

        try:
            result = subprocess.run(
                [
                    'python3',
                    str(run_py_path),
                    str(
                        self.config_file_path.relative_to(
                            self.nvm_explorer_path))
                ],
                check=True,
                capture_output=True,
                text=True,
                cwd=self.
                nvm_explorer_path  # Set the child directory as the working directory
            )
            print("Run Output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error running run.py:", e.stderr)

        # read outputs from nvm_explorer
        self.read_output()
        self.add_lifetime_data()

    def save_config(self):
        '''Saves config file in nvmexplorer's configs directory'''

        with self.config_file_path.open('w') as file:
            json.dump(self.config, file, indent=4)
        print(f"Configuration saved to {self.config_file_path}")

    def read_output(self):
        '''Extracts data from nvmexplorer's output directory'''
        results_path = self.get_results_path()
        df = pd.read_csv(results_path)
        self.results = df.iloc[0]
        return

    def print_summary(self):
        '''Prints out entire results dataset.'''
        print("Summary:")
        print("------------------------")
        for key, value in self.results.items():
            print(f"{key}: {value}")
    
    def get_result(self, result_type: ResultType):
        '''Gets specific result from output dataframe'''
        if self.results is None:
            raise Exception(
                f"Results not found. Make sure to run model first."
            )

        return self.results[result_type.value]

    def update_config(self, row_name: str, value):
        '''Updates cell configuration.'''
        if row_name not in self.config["experiment"]:
            raise Exception("Invalid row name.")
        
        if row_name in ("cell_type", "opt_target", "capacity", "bits_per_cell"):
            value = [value]
        
        self.config["experiment"][row_name] = value
        return
    
    def get_config_val(self, row_name: str):
        if row_name not in self.config["experiment"]:
            raise Exception(f"Invalid row name: {row_name}")
    
        if row_name in ("cell_type", "opt_target", "capacity", "bits_per_cell"):
            return self.config["experiment"][row_name][0]
        else:
            return self.config["experiment"][row_name]
        
    def get_config_vals(self, row_names: List[str]):
        vals = []
        for row_name in row_names:
            vals.append(self.get_config_val(row_name))
        return vals

    def get_results_path(self):
        cell_value, capacity, opt_target, bits_per_cell = self.get_config_vals(["cell_type", "capacity", "opt_target", "bits_per_cell"])
        return self.nvm_explorer_path / "output" / "results" / f"{cell_value}_{capacity}MB_{opt_target}_{bits_per_cell}BPC-default.csv"
    
    def add_lifetime_data(self):
        endurancedf_path = self.nvm_explorer_path / "EducationalTutorial" / "2016-2020_EnduranceSummary.csv"
        endurancedf = pd.read_csv(endurancedf_path)

        cell_type = self.get_result(ResultType.MEM_CELL_TYPE).strip()
        if cell_type == 'SRAM':
            return

        minEndurance = endurancedf[(endurancedf['Memory Cell'] == cell_type)]['min'].iloc[0]
        
        # We do not have enough data on the max endurance of some of the cells so if null, we just equal it to the minimum
        maxEndurance = endurancedf[(endurancedf['Memory Cell'] == cell_type) & (endurancedf['max'].notnull())]['max'].iloc[0]

        min_life_expectancy = minEndurance if self.get_result(ResultType.WRITE_ACCESSES) != 0.0 else 3.2e8
        max_life_expectancy = maxEndurance if self.get_result(ResultType.WRITE_ACCESSES) != 0.0 else 3.2e8

        # add result as a touple to results dataframe
        self.results["Life Expectancy (s)"] = (min_life_expectancy, max_life_expectancy)

    def cleanup(self):
        '''Cleans up nvmexplorer directory. Should be run after done using model.'''
        # delete config file
        if self.config_file_path.exists():
            self.config_file_path.unlink()

        # clear results directory
        results_dir_path = self.nvm_explorer_path / "output" / "results"
        if results_dir_path.exists() and results_dir_path.is_dir():
            shutil.rmtree(results_dir_path)

        # clear logs directory
        logs_dir_path = self.nvm_explorer_path / "output" / "logs"
        if logs_dir_path.exists() and logs_dir_path.is_dir():
            shutil.rmtree(logs_dir_path)

        # clear nvsim_output directory
        nvsim_output_dir_path = self.nvm_explorer_path / "output" / "nvsim_output"
        if nvsim_output_dir_path.exists() and nvsim_output_dir_path.is_dir():
            shutil.rmtree(nvsim_output_dir_path)

        # clear mem_cfs directory
        mem_cfs_dir_path = self.nvm_explorer_path / "data" / "mem_cfgs"
        if mem_cfs_dir_path.exists() and mem_cfs_dir_path.is_dir():
            shutil.rmtree(mem_cfs_dir_path)

        print("Cleanup complete.")
        return

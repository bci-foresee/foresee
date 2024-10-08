import json
import os
import shutil
import subprocess
from enum import Enum
import pandas as pd
from utils import CellType, OpTarget


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

class StorageModel:
    """
    A class to model storage performance from various workload and cell configurations.
    """
    def __init__(self, 
                 read_frequency: int, 
                 write_frequency: int, 
                 read_size: int, 
                 write_size: int, 
                 cell_type: CellType, 
                 word_width: int=16,
                 process_node: int=22, 
                 opt_target: OpTarget=OpTarget.ReadLatency, 
                 capacity: int=1,
                 bits_per_cell: int=1):
        self.config = {
            "experiment": {
                "read_frequency": read_frequency,
                "write_frequency": write_frequency,
                "read_size": read_size,
                "write_size": write_size,
                "cell_type": [cell_type.value],
                "process_node": process_node, #TODO: figure out what this does / why it doesn't trigger new output file
                "opt_target": [opt_target.value],
                "word_width": word_width,
                "capacity": [capacity],
                "bits_per_cell": [bits_per_cell],
                "nvsim_path": "./nvmexplorer_src/nvsim_src/nvsim",
                "output_path": "./output",
            }
        }
        self.worst_case = None
        self.best_case = None
        self.config_file_path = "nvmexplorer/config/storage_model.json"
        self.results_path = "nvmexplorer/output/results/{}_{}MB_{}_{}BPC-default.csv".format(
            cell_type.value, capacity, opt_target.value, bits_per_cell) 
    
    def run(self):
        '''Runs model in nvmexplorer.'''
        print("Running model...")
        # save config file in nvmexplorer
        self.save_config(self.config_file_path)
        
        # run nvmexplorer
        run_py_path = os.path.join(os.path.dirname(__file__), 'nvmexplorer', 'run.py')
        child_dir = os.path.join(os.path.dirname(__file__), 'nvmexplorer')

        try:
            result = subprocess.run(
                ['python3', run_py_path, self.config_file_path.replace("nvmexplorer/", "", 1)],
                check=True,
                capture_output=True,
                text=True,
                cwd=child_dir  # Set the child directory as the working directory
            )
            print("Run Output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error running run.py:", e.stderr)

        # read outputs from nvm_explorer
        self.read_output()

    def save_config(self, file_path):
        '''Saves config file in nvmexplorer's configs directory'''
        with open(file_path, 'w') as file:
            json.dump(self.config, file, indent=4)
        print(f"Configuration saved to {file_path}")
    
    def read_output(self):
        '''Extracts best case and worst case data from nvmexplorer's output directory'''
        df = pd.read_csv(self.results_path)
        self.worst_case = df.iloc[0]
        self.best_case = df.iloc[1]
        return

    def display_summary(self):
        '''Prints out best case and worst case performance data'''
        print("Worst Case Cell Summary:")
        print("------------------------")
        for key, value in self.worst_case.items():
            print(f"{key}: {value}")
        print("\nBest Case Cell Summary:")
        print("------------------------")
        print(self.best_case)
        for key, value in self.best_case.items():
            print(f"{key}: {value}")
    
    def cleanup(self):
        '''Cleans up nvmexplorer directory. Should be run after done using model.'''
        # delete config file
        if os.path.exists(self.config_file_path):
            os.remove(self.config_file_path)

        # clear results directory
        results_dir_path = "nvmexplorer/output/results"
        if os.path.exists(results_dir_path) and os.path.isdir(results_dir_path):
            shutil.rmtree(results_dir_path)

        # clear logs directory
        logs_dir_path = "nvmexplorer/output/logs"
        if os.path.exists(logs_dir_path) and os.path.isdir(logs_dir_path):
            shutil.rmtree(logs_dir_path)

        # clear nvsim_output directory
        nvsim_output_dir_path = "nvmexplorer/output/nvsim_output"
        if os.path.exists(nvsim_output_dir_path) and os.path.isdir(nvsim_output_dir_path):
            shutil.rmtree(nvsim_output_dir_path)
        
        # clear mem_cfs directory
        mem_cfs_dir_path = "nvmexplorer/data/mem_cfgs"
        if os.path.exists(mem_cfs_dir_path) and os.path.isdir(mem_cfs_dir_path):
            shutil.rmtree(mem_cfs_dir_path)

        print("Cleanup complete.")
        return

import json
import shutil
import subprocess
from enum import Enum
import pandas as pd
from pathlib import Path
from storage.utils import CellType, OpTarget

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
                 word_width: int = 16,
                 process_node: int = 22, #TODO: figure out what this does / why it doesn't trigger new output file
                 opt_target: OpTarget = OpTarget.ReadLatency,
                 capacity: int = 1,
                 bits_per_cell: int = 1):
        self.nvm_explorer_path = Path(__file__).resolve().parent / "nvmexplorer"
        self.config = {
            "experiment": {
                "read_frequency": read_frequency,
                "write_frequency": write_frequency,
                "read_size": read_size,
                "write_size": write_size,
                "cell_type": [cell_type.value],
                "process_node": process_node,
                "opt_target": [opt_target.value],
                "word_width": word_width,
                "capacity": [capacity],
                "bits_per_cell": [bits_per_cell],
                "nvsim_path": str(self.nvm_explorer_path / "nvmexplorer_src" / "nvsim_src" / "nvsim"),
                "output_path": str(self.nvm_explorer_path / "output"),
            }
        }
        self.worst_case = None
        self.best_case = None
        self.config_file_path = self.nvm_explorer_path / "config" / "storage_model.json"
        self.results_path = self.nvm_explorer_path / "output" / "results" / f"{cell_type.value}_{capacity}MB_{opt_target.value}_{bits_per_cell}BPC-default.csv"

    def run(self):
        '''Runs model in nvmexplorer.'''
        print("Running model...")
        # check if nvsim executable exists
        nvsim_path =  self.nvm_explorer_path / "nvmexplorer_src" / "nvsim_src" / "nvsim"
        if not nvsim_path.exists():
            raise FileNotFoundError(f"NVSim executable does not exist. Write 'make' in {nvsim_path.parent()}.")
        
        # save config file in nvmexplorer
        self.save_config()

        # run nvmexplorer
        run_py_path = self.nvm_explorer_path / 'run.py'

        try:
            result = subprocess.run(
                [
                    'python3', str(run_py_path),
                    str(self.config_file_path.relative_to(self.nvm_explorer_path))
                ],
                check=True,
                capture_output=True,
                text=True,
                cwd=self.nvm_explorer_path  # Set the child directory as the working directory
            )
            print("Run Output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error running run.py:", e.stderr)

        # read outputs from nvm_explorer
        self.read_output()

    def save_config(self):
        '''Saves config file in nvmexplorer's configs directory'''
        
        with self.config_file_path.open('w') as file:
            json.dump(self.config, file, indent=4)
        print(f"Configuration saved to {self.config_file_path}")

    def read_output(self):
        '''Extracts best case and worst case data from nvmexplorer's output directory'''
        df = pd.read_csv(self.results_path)
        self.worst_case = df.iloc[0]
        self.best_case = df.iloc[1]
        return

    def print_summary(self):
        '''Prints out best case and worst case performance data'''
        print("Worst Case Cell Summary:")
        print("------------------------")
        for key, value in self.worst_case.items():
            print(f"{key}: {value}")
        print("\nBest Case Cell Summary:")
        print("------------------------")
        for key, value in self.best_case.items():
            print(f"{key}: {value}")

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
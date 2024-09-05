Unfinished notes on setting up new system to run this project.

## Conda environment

```sh
conda env create -f environment.yaml
conda activate scalo_sim
```

Check installation:
```sh
conda list
```

## iverilog/vvp

```sh
sudo apt update
sudo apt install iverilog
```

Check installation:
```sh
iverilog -v
```
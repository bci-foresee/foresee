#!/bin/bash
#source
source /home/sy587/anaconda3/etc/profile.d/conda.sh
# Initialize conda
eval "$(/home/sy587/anaconda3/bin/conda shell.bash hook)"
# Activate the conda environment
conda activate scalo_sim
# Add any commands you want to run after activating the environment
echo "Conda environment 'scalo_sim' activated (nvm doesnt work yet for some reason)"

# init 
git init

# iverilog/vvp
sudo apt update
sudo apt install iverilog
iverilog -v

# power estimation
sudo apt-get update
sudo apt-get install flex libeigen3-dev autoconf automake

#pygraphviz
sudo apt-get update
sudo apt-get install graphviz libgraphviz-dev pkg-config

# Conda set up
conda env create -f environment.yaml
conda activate scalo_sim
conda list

# setting up submodules
git rm -rf external/
git rm --cached external/cudd
git rm --cached external/OpenSTA
git rm .gitmodules
echo "" > .gitmodules

# cudd
git submodule add --force https://github.com/ivmai/cudd.git external/cudd
git submodule init
git submodule update
cd external/cudd/
autoreconf -vif
./configure --prefix=/usr/local
sudo make install
cd ../..

# openSTA
git submodule add --force https://github.com/The-OpenROAD-Project/OpenSTA.git external/OpenSTA
git submodule init
git submodule update
cd external/OpenSTA/
mkdir build
cd build
cmake ..
make #make -j$(2) this could be faster
../app/sta --version
cd ../../..

# yosys
sudo apt-get install yosys
yosys -V
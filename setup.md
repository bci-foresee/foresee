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

## power estimation


import openSTA as a gitmodule

make build folder and build it

get flex (not on codespaces)
libgen3-dev
autoconf automake
```sh
sudo apt-get update
sudo apt-get install flex libeigen3-dev autoconf automake
```


CUDD
clone from git:
```sh
git submodule add https://github.com/ivmai/cudd.git external/cudd
git submodule init
git submodule update
cd external/cudd/
autoreconf -vif
./configure --prefix=/usr/local
sudo make install
cd ../..
```


Then make openSTA
```sh
git submodule add https://github.com/The-OpenROAD-Project/OpenSTA.git external/OpenSTA
git submodule init
git submodule update
cd external/OpenSTA/
mkdir build
cd build
cmake ..
make #make -j$(2) this could be faster
../app/sta --version
# export PATH=$PATH:/workspaces/power-estimation/external/OpenSTA/app 
# ^ that might be needed to run sta globally, may need to run this again if you close the terminal.
# in order to perma - do this
# echo "export PATH=$PATH:/workspaces/power-estimation/external/OpenSTA/app" >> ~/.bashrc
# ^^ put this generalised outside
cd ../../..
```

Yosys
```sh
sudo apt-get install yosys
```


Check versions
```sh
yosys -V
```

To run:
```sh
yosys -s synth.ys
iverilog -o clocked_adder clocked_adder_tb.v clocked_adder.v
vvp clocked_adder
sta power_sta.tcl
```

## Notes

the .ys file is a yosys script file. It is a text file that contains commands that yosys will execute. The -s flag tells yosys to run the commands in the file.

The .tcl file is a tcl script file. It is a text file that contains commands that the tcl interpreter will execute. The sta command is a tcl command that runs the sta tool.

.tcl contains how to run the openSTA tool. ie do you want to report power etc
full documentation: [link](https://github.com/The-OpenROAD-Project/OpenSTA/blob/master/doc/OpenSTA.pdf)
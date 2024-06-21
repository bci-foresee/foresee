notes, unfinished.

```sh
verilator -Wall --cc --exe counter.v tb_counter.cpp 

cd obj_dir  

make -f Vcounter.mk

./Vcounter
```

and it works!


new from inside Simulator-Dev
```sh
verilator --cc ./Verilog_Dev_Items/top.v ./Verilog_Dev_Items/counter.v ./Verilog_Dev_Items/bit_checker.v --exe top_tb.cpp

cd obj_dir

make -f Vtop.mk

./Vtop
```

In order to change testbench in c only need to run the following again:
```sh
make -f Vtop.mk
./Vtop
```


Sim stable: <--- example is here as of now.

```sh
verilator -cc ./Verilog-APaths/example_top.v ./Verilog-PEs/adder.v --exe example_tb.cpp
cd obj_dir
make -f Vexample_top.mk
./Vexample_top
```

```sh
verilator -Wall --cc --exe counter.v tb_counter.cpp 

cd obj_dir  

make -f Vcounter.mk

./Vcounter
```

and it works!
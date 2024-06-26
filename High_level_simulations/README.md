

create a c file, ie `svm.cpp`

then run *(linux only)*:
```sh
g++ -shared -o [library_name].so -fPIC [c_models].cpp
```

you can see in svm_test.py how to then call the function.
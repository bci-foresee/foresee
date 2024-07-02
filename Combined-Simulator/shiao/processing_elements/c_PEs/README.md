# Shiao Pipeline

Seizure Detection Pipeline from https://ieeexplore.ieee.org/document/7501827

```sh
g++ -shared -o libkernels.so -fPIC kernels.cpp
```

# Tests

Written using pytest. To run, go to `High_level_simulations/shiao` then run

```sh
pytest -v test_shiao.py
```

## FFT
https://www.spiral.net/doc/usermanual/examples/basic/firstfft.html

## BBF
Populate 'filters' using mkfilter: https://github.com/MikeCurrington/mkfilter/blob/master/doc.pdf

There will be six functions corresponding to each Berger band. This requires the sampling frequency 
($SF) which is 30000 Hz for now. The following are the cutoff frequencies ($LF, $UF):
(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 120). Run mkfilter for each cutoff. Order ($ORD) is also
a parameter to the filter which can range from 1-10 and is specified using -o. We set the default to 5.

./mkfilter -Bu -Bp -o $ORD -a $($LF/$SF) $($UF/$SF) -l | ./gencode

The generated code needs to be transformed into a function that takes in a single sample and outputs a single value. 
Then, run each sample in the input signal through the six filters and calculate the sum of the squares of each output
for each filter. This will be the 'power' in the six bands. 

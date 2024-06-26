This directory is here somewhat temporarily.

It is here essentially to provide a place to put work such as the FFT in C generation from Spiral so that there is a reference of the process and reproducability.

- FFT: https://www.spiral.net/doc/usermanual/examples/index.html#basic-ffts

Get spiral-software-master from: https://github.com/spiral-software/spiral-software
and then run

To run sprial cd to spiral-software-master then

```sh
./bin/spiral
```

I am generating the fft with a random rule tree, a deep search into the space can provide a more optimal rule tree that will almost certainly be faster than the one implemented (https://www.spiral.net/doc/usermanual/examples/basic/dpsearch.html). As we currently only care about the logic being correct in the tester, I am not going to spend time on finding an optimal rule tree for c.

Spiral code for 1024 fft
```
opts := SpiralDefaults;
transform := DFT(1024);
ruletree := RandomRuleTree(transform, opts);
icode := CodeRuleTree(ruletree, opts);
PrintCode("DFT1024", icode, opts);
```

generated code is in ./spiral-fft.c


- mkfilter: https://github.com/MikeCurrington/mkfilter

How to use:

Download files from link shown

Then `make` in the ./mkfilter-master directory

example in halo is:
```
./mkfilter -Bu -Bp -o 5 -a 7.5000000000e-02 2.0000000000e-01 -l | ./gencode

- Bu: Butterworth filter
- Bp: Bandpass filter

- o: order of the filter, essentially how steep the cutoff is

- a: bandpass cutoff ratio.
        ie if sampling rate is 1Khz and want a bandpass from 250Hz to 750Hz
        then a = 250/1000 = 0.25 and b = 750/1000 = 0.75 => -a 0.25 0.75

- l: make a lowpass filter first and then convert it into a bandpass filter

- | ./gencode: pipe the output of mkfilter into gencode to generate the c code

```

- note halo paper butterworth.c uses the command `/mkfilter -Bu -Bp -o 5 -a 7.5000000000e-02 2.0000000000e-01 -l` which implies a sampling rate of 400Hz (should be 30000Hz? inconsistency?)

Going off of 400Hz in shiao paper

bandpass filter ranges (Hz):
(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 120)

commands, assuming 400Hz sampling rate:
```sh
./mkfilter -Bu -Bp -o 5 -a 0.00025 0.01 -l | ./gencode
./mkfilter -Bu -Bp -o 5 -a 0.01 0.02 -l | ./gencode
./mkfilter -Bu -Bp -o 5 -a 0.02 0.03 -l | ./gencode
./mkfilter -Bu -Bp -o 5 -a 0.03 0.075 -l | ./gencode
./mkfilter -Bu -Bp -o 5 -a 0.075 0.2 -l | ./gencode
./mkfilter -Bu -Bp -o 5 -a 0.2 0.3 -l | ./gencode
```

generated code is in ./mkfilter-butterworth.c

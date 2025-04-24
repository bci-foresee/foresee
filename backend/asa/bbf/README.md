# Butterworth Bandpass Filter (BBF)

## mkfilter
* [Information](https://github.com/MikeCurrington/mkfilter/blob/master/doc.pdf)
* [Repository](https://github.com/MikeCurrington/mkfilter)

### Generate BBF
```sh
git clone git@github.com:MikeCurrington/mkfilter.git
cd mkfilter
make
```

HALO example:

```sh
./mkfilter -Bu -Bp -o 5 -a 7.5000000000e-02 2.0000000000e-01 -l | ./gencode
```
(TODO: There are inconsistencies with the above command which implies a sampling rate of 400 Hz instead of 30000 Hz)

Berger Bands example:

* Assuming a 400 Hz sampling rate
* Cutoff frequencies -- (0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 120)

```sh
./mkfilter -Bu -Bp -o 5 -a 0.00025 0.01 -l | ./gencode
./mkfilter -Bu -Bp -o 5 -a 0.01 0.02 -l | ./gencode
./mkfilter -Bu -Bp -o 5 -a 0.02 0.03 -l | ./gencode
./mkfilter -Bu -Bp -o 5 -a 0.03 0.075 -l | ./gencode
./mkfilter -Bu -Bp -o 5 -a 0.075 0.2 -l | ./gencode
./mkfilter -Bu -Bp -o 5 -a 0.2 0.3 -l | ./gencode
```

Options:

- `-Bu` -- Butterworth filter
- `-Bp` -- Bandpass filter
- `-o` -- order of the filter, essentially how steep the cutoff is
- `-a` -- bandpass cutoff ratio, i.e., if sampling rate is 1Khz and want a bandpass from 250Hz to 750Hz then a = 250/1000 = 0.25 and b = 750/1000 = 0.75 => -a 0.25 0.75
- `-l` -- make a lowpass filter first and then convert it into a bandpass filter
- `| ./gencode` -- pipe the output of mkfilter into `./gencode` to generate the C code
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
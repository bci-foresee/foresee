# Fast Fourier Transform (FFT)

## Spiral
* [Information](https://www.spiral.net/doc/usermanual/examples/index.html#basic-ffts)
* [Repository](https://github.com/spiral-software/spiral-software)

### Generate FFT
Build Spiral from source and run:

```sh
./bin/spiral
```

The following generates with a random rule tree, a deep search into the space can provide a more optimal rule tree that will almost certainly be faster than the one implemented (https://www.spiral.net/doc/usermanual/examples/basic/dpsearch.html). As we currently only care about the logic being correct in the tester, I am not going to spend time on finding an optimal rule tree for c.

Spiral code for 1024 fft
```
opts := SpiralDefaults;
transform := DFT(1024);
ruletree := RandomRuleTree(transform, opts);
icode := CodeRuleTree(ruletree, opts);
PrintCode("DFT1024", icode, opts);
```

Generated code is in ./spiral-fft.c
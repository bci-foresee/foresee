
fft_magnitude_spectrum_artifacts show semi working ffts

- artifact 1
    - working fft but breaks down due to sample float -> int conversion I think

- artifact 2
    - when I multiply floats by 100 before converting to int. Slightly better

- artifact 3
    - when I multiply floats by 10_000 before converting to int. Slightly better, but there is a lot of loss of info.
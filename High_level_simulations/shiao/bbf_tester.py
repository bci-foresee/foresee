import numpy as np
from pipeline import Pipeline
pipeline = Pipeline(kernel_lib='libkernels.so')

def test_bbf():
    #dummy signal to sample
    def signal(x):
        # return np.ones_like(x)
        return 10*np.sin(x) + 5*np.sin(2*x) + 2*np.sin(3*x) + 1*np.sin(4*x)
    
    #dummy data
    sample_rate = 400 #Hz, how many samples per second
    num_samples = 8000 # how many samples fed into bbf <- may need to change

    sample_window = (1/sample_rate) * num_samples # seconds, how much time the samples are taken over around 2.56 seconds

    # taking samples
    sample_space = np.linspace(0, sample_window * 2 * np.pi, num_samples) # assuming 2 pi radians per second
    signal_samples = signal(sample_space)
    signal_samples = np.array(signal_samples, dtype=np.uint16)

    # print("...signal_samples...")
    # print(len(signal_samples))
    # print(signal_samples[:10])

    # choose gain, filter vals
    chosen_bandpass = "30-80"
    gain, filter_vals = give_me_bbf_values(chosen_bandpass)

    #printing all the inputs that go in
    print("...inputs...")
    print("chosen band: ", chosen_bandpass)
    print("signal_in: ", signal_samples[:10], "...")
    print("filter_vals[0,1]: ", filter_vals[0:2])
    print("filter_vals[2,3]: ", filter_vals[2:4])
    print("filter_vals[4,5]: ", filter_vals[4:6])
    print("filter_vals[6,7]: ", filter_vals[6:8])
    print("filter_vals[8,9]: ", filter_vals[8:10])
    print("gain: ", gain)
    print("num_points: ", num_samples)
    print()

    # calling the c function, result is power in a certain band (need to implement band part)
    result = pipeline.bbf(signal_in=signal_samples, 
                          filter_vals=filter_vals, 
                          gain=gain,
                          num_points=num_samples)

    #printing the output:
    print("...output...")
    print("result: ", result)
    print()

    assert result == result - 1 + 1 , "Test not implemented"

def give_me_bbf_values(filter_range):
    if filter_range == "30-80":
        filter_vals = np.array([
             -0.0723156691,  0.6368872577,
             -2.8198218361,  8.0640603736,
            -16.3818055300, 24.6025699180,
            -27.6694600560, 23.0616757780,
            -13.6958889160,  5.2541969233
            ], dtype=np.double)
        gain =  3.049509079e+02
        return (gain, filter_vals)


"-------------"
from scipy.signal import butter, filtfilt
 
SAMPLING_FREQ = 400

BANDS = [(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)]


def bbf(signal):
    """
    'signal' is an array of values corresponding to a time window
    """
    result = []
    for band in BANDS:
        order = 5
        low_freq = band[0] / (SAMPLING_FREQ / 2.0) # why is it div by 2?
        high_freq = band[1] / (SAMPLING_FREQ / 2.0)
        # low_freq = band[0] / (SAMPLING_FREQ)
        # high_freq = band[1] / (SAMPLING_FREQ)
        # print("low_freq: ", low_freq)
        # print("high_freq: ", high_freq)
        b, a = butter(order, [low_freq, high_freq], btype="bandpass")
        # print(b[10])
        filtered_signal = filtfilt(b, a, signal)
        # print(len(filtered_signal))
        power_est = np.dot(filtered_signal, filtered_signal)
        result.append(power_est)
    return result

test_bbf()

def signal(x):
        # return np.ones_like(x)
        return 10*np.sin(x) + 5*np.sin(2*x) + 2*np.sin(3*x) + 1*np.sin(4*x)
    
#dummy data
sample_rate = 400 #Hz, how many samples per second
num_samples = 8000 # how many samples fed into bbf <- may need to change

sample_window = (1/sample_rate) * num_samples # seconds, how much time the samples are taken over around 2.56 seconds

# taking samples
sample_space = np.linspace(0, sample_window * 2 * np.pi, num_samples) # assuming 2 pi radians per second
signal_samples = signal(sample_space)
signal_samples = np.array(signal_samples, dtype=np.uint16)

print("...test 2 bbf...")
out = bbf(signal_samples)
print(out)
print("30-80: ", out[4])
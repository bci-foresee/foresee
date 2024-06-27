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
    chosen_bandpass = "8-12"
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

    print("...test 2 bbf...")
    out = expected_bbf(signal_samples)
    print(out)
    print("8-12: ", out[2])

    assert result == result - 1 + 1 , "Test not implemented"

def give_me_bbf_values(filter_range):
    if filter_range == "0.1-4":
        filter_vals = np.array([
            -0.8201374968  ,  8.3635427995  ,
            -38.3822761210 ,  104.3882390000,
            -186.3227066700, 228.0589411300 ,
            -193.8606607400, 113.0053670900 ,
            -43.2315892410 ,  9.8012802461
            ], dtype=np.double)
        gain =  5.890713166e+08
        return (gain, filter_vals)
    
    elif filter_range == "4-8":
        filter_vals = np.array([
            -0.8159766800   ,  8.2928122581, 
            -37.9613651660  ,103.0719262700, 
            -183.8272415500 ,225.0212908000,
            -191.4589373100 ,111.8076742600,
            -42.8882014600  ,  9.7580185732 
            ], dtype=np.double)
        gain = 3.616929452e+07
        return (gain, filter_vals)
    
    elif filter_range == "8-12":
        filter_vals = np.array([
            -0.8159766800  ,  8.2272267013, 
            -37.4301796450 ,101.1853826500, 
            -179.9897686400,220.1314527600,
            -187.4621386000,109.7612297700,
            -42.2880734300 ,  9.6808451053 
            ], dtype=np.double)
        gain = 3.611451395e+07
        return (gain, filter_vals)
    
    elif filter_range == "12-30":
        filter_vals = np.array([
            -0.3990100050  , 4.1615662713 ,
            -19.7568686440 ,56.2070319960 ,
            -106.0979110400,138.8326180500,
            -127.5312431000, 81.2061196740,
            -34.3049564260 ,  8.6826497480 
            ], dtype=np.double)
        gain =  2.711202696e+04
        return (gain, filter_vals)

    elif filter_range == "30-80":
        filter_vals = np.array([
             -0.0723156691,  0.6368872577,
             -2.8198218361,  8.0640603736,
            -16.3818055300, 24.6025699180,
            -27.6694600560, 23.0616757780,
            -13.6958889160,  5.2541969233
            ], dtype=np.double)
        gain =  3.049509079e+02
        return (gain, filter_vals)
    
    elif filter_range == "80-120":
        filter_vals = np.array([
            -0.1254306222,0.0000000000,
            -0.8811300754,0.0000000000,
            -2.5452528683,0.0000000000,
            -3.8060181193,0.0000000000,
            -2.9754221097,0.0000000000
            ], dtype=np.double)
        gain =  7.796778047e+02
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

def expected_bbf(signal):
    SAMPLING_FREQ = 400
    BANDS = [(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)]

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
import numpy as np
from pipeline import Pipeline
pipeline = Pipeline(kernel_lib='libkernels.so')

def test_bbf():
    #dummy signal to sample
    def signal(x):
        return np.sin(x)
    
    #dummy data
    sample_rate = 400 #Hz, how many samples per second
    num_samples = 1024 # how many samples fed into bbf <- may need to change

    sample_window = (1/sample_rate) * num_samples # seconds, how much time the samples are taken over around 2.56 seconds

    # taking samples
    sample_space = np.linspace(0, sample_window * 2 * np.pi, num_samples) # assuming 2 pi radians per second
    signal_samples = signal(sample_space)
    signal_samples = np.array(signal_samples, dtype=np.uint16)

    # choose gain, filter vals
    gain, filter_vals = give_me_bbf_values("0.1-4")

    # calling the c function, result is power in a certain band (need to implement band part)
    result = pipeline.bbf(signal_in=signal_samples, 
                          filter_vals=filter_vals, 
                          gain=gain,
                          num_points=num_samples)

    print(result)

    assert result == result - 1 + 1 , "Test not implemented"

def give_me_bbf_values(filter_range):
    if filter_range == "0.1-4":
        filter_vals = np.array([
            -0.8201374968, 8.3635427995,
            -38.3822761210,  104.3882390000,
            -186.3227066700, 228.0589411300,
            -193.8606607400, 113.0053670900,
            -43.2315892410,  9.8012802461], dtype=np.double)
        gain =  5.890713166e+08
        return (gain, filter_vals)
    

test_bbf()
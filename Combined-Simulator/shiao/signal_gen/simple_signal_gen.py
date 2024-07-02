import numpy as np
import matplotlib.pyplot as plt

def sample_signals(num_signals, sample_window, num_samples, saveGraphs=False):

    # define a sampled function, and the sample
    def signal1(t):
        # frequencies = [10, 50, 80, 125]
        # amplitudes =  [20,  15,  15,  5]
        frequencies = [5]
        amplitudes =  [20]
        returnSignal = 0
        for i in range(len(frequencies)):
            returnSignal += amplitudes[i] * np.sin(2*np.pi*frequencies[i]*t)  
        return (returnSignal)
    
    def randomvals(t):
        return np.ones_like(t)
    
    sampled_signals = []
    for i in range(num_signals):
        x = np.linspace(start=0, stop=sample_window, num=num_samples, endpoint=False)
        if i == 0:
            sampled_signals.append(signal1(x))
            # display 1st sampled signal
            if saveGraphs:
                plt.figure(figsize=(12, 6))
                plt.plot(x, sampled_signals[0])
                plt.title('Sampled Signal')
                plt.xlabel('Time (s)')
                plt.ylabel('Amplitude')
                plt.grid()
                plt.savefig('plots/seizure_pipe/sampled_signal.png')

                # also printing int converted graph
                int_sampled_signal = [int(sampled_signals[0][i]) for i in range(len(sampled_signals[0]))]
                plt.figure(figsize=(12, 6))
                plt.plot(x, int_sampled_signal)
                plt.title('Sampled Signal int conversion')
                plt.xlabel('Time (s)')
                plt.ylabel('Amplitude')
                plt.grid()
                plt.savefig('plots/seizure_pipe/sampled_signal_int.png')
        else:
            sampled_signals.append(randomvals(x))

    return sampled_signals
import numpy as np
from scipy import signal
from line_profiler import LineProfiler

def your_compute_function(x, y):
    z = np.add(x, y)
    return signal.convolve(z, np.ones(1000))

# Prepare some sample data
x = np.random.rand(1000)
y = np.random.rand(1000)

# Set up the profiler
lp = LineProfiler()
lp_wrapper = lp(your_compute_function)

# Run the profiled function
result = lp_wrapper(x, y)

# Print the results
lp.print_stats()
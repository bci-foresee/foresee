import cProfile
import pstats
import io
import numpy as np
from scipy import signal


def your_compute_function(x, y):
    z = np.add(x, y)
    return signal.convolve(z, np.ones(10))


# Prepare some sample data
x = np.random.rand(1000)
y = np.random.rand(1000)

# Profile the function
pr = cProfile.Profile()
pr.enable()
result = your_compute_function(x, y)
pr.disable()

# Print the results
s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
ps.print_stats()
print(s.getvalue())

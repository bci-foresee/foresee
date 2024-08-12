import numpy as np
from scipy import signal
from line_profiler import LineProfiler

def your_compute_function(x, y):
    z = np.add(x, y)
    return signal.convolve(z, np.ones(1000))

# Prepare some sample data
x = np.random.rand(10000)
y = np.random.rand(10000)

# Set up the profiler
lp = LineProfiler()
lp_wrapper = lp(your_compute_function)

# Run the profiled function
result = lp_wrapper(x, y)

# Print the profiling results
lp.print_stats()

# Example power estimation function
def estimate_power_from_line_profile(stats, power_weights):
    total_power = 0
    for key, timings in stats.timings.items():
        print(key, timings)
        for line_no, hits, total_time in timings:
            for operation, weight in power_weights.items():
                # We'll use the total_time as a proxy for operation complexity
                if operation in stats.timings:
                    print(f"hits: {hits}, weight: {weight}, total_time: {total_time}")
                    total_power += hits * weight * (total_time / 1e6)  # Convert time to seconds
    return total_power

# Example power weights (you'd need to determine these based on your RTL knowledge)
power_weights = {
    'add': 10,
    'convolve': 100,
    # Add more operations and weights as needed
}

# Estimate power consumption
estimated_power = estimate_power_from_line_profile(lp.get_stats(), power_weights)
print(f"Estimated power consumption: {estimated_power}")

# should do something of the sort like 
# how much time spent on how many computations
# total time spent
# use to calculate latency estimate
# use to calculate dynamic power estimate
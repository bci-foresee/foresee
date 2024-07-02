
'''
##################################

This module returns 1 if the value is within the bounds, 0 otherwise.

# Inputs
- val [float]                          value to be checked
- upper_bound [float]                  upper bound
- lower_bound [float]                  lower bound

# Outputs
- output [int]                         1 if val is within bounds, 0 otherwise

##################################
'''


def thr_py(val, upper_bound, lower_bound):
    if (val >= lower_bound) and (val <= upper_bound):
        return 1
    else:
        return 0
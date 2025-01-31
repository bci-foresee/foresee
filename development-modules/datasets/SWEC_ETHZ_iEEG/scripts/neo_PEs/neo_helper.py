import numpy as np
from numpy.typing import NDArray


def tkeo_py(input: NDArray[np.float64]) -> NDArray[np.float64]:
    """
    Vectorized implementation of TKEO computation for multiple channels
    
    Args:
        input: Input signal array of shape (n_channels, n_samples)
                where n_channels is the number of channels and
                n_samples is the number of samples per channel
        
    Returns:
        NDArray containing TKEO values for all channels, shape (n_channels, n_samples)
    """
    # Ensure input is 2D array
    if input.ndim == 1:
        input = input.reshape(1, -1)

    # Convert input to float64 if it isn't already
    input = input.astype(np.float64)

    # Get dimensions
    n_channels, n_samples = input.shape

    # Initialize output array
    output = np.zeros_like(input)

    # Compute main TKEO values using vectorized operations for all channels
    output[:, 1:-1] = input[:, 1:-1]**2 - input[:, :-2] * input[:, 2:]

    # Handle edge cases for all channels
    output[:, 0] = input[:, 0]**2 - input[:, 0] * input[:, 1]
    output[:, -1] = input[:, -1]**2 - input[:, -2] * input[:, -1]

    return output


def avg_py(input: NDArray[np.float64]) -> NDArray[np.float64]:
    """
        Vectorized implementation of AVG computation for multiple channels

        Args:

            input: Input signal array of shape (n_channels, n_samples)
                    where n_channels is the number of channels and
                    n_samples is the number of samples per channel

        Returns:
            NDArray containing AVG values for all channels
        """

    return np.mean(input, axis=1)

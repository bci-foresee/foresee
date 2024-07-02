import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

'''
##################################

This module takes in a list of sampled signals and calculates the cross-correlation between each pair of signals.

Each xcorr value is then returned (ie 16 signals => 120 xcorr values)

# Inputs
- sampled_signals [np.array::float]     list of sampled signals
- num_channels [int]                     number of channels to generate
- saveGraphs [Bool]                      boolean determining if graphs are generated

# Outputs
- correlations [np.array::float]         list of cross-correlation values
- corr_matrix [png]                      plot of the correlation matrix

##################################
'''

def xcorr_py(sampled_signals, num_channels, saveGraphs=False):
    correlations = []

    # Calculate normalized cross-correlations
    for i in range(num_channels):
        for j in range(i + 1, num_channels):
            corr = np.correlate(sampled_signals[i], sampled_signals[j], mode='valid')[0]
            norm_corr = corr #/ (num_samples * np.std(sampled_signals[i]) * np.std(sampled_signals[j]))
            correlations.append(norm_corr)

    # Convert the correlations list into a correlation matrix
    def create_correlation_matrix(correlations, num_channels):
        corr_matrix = np.zeros((num_channels, num_channels))
        idx = 0
        for i in range(num_channels):
            for j in range(i + 1, num_channels):
                corr_matrix[i, j] = correlations[idx]
                idx += 1
        corr_matrix += corr_matrix.T  # Make it symmetric
        return corr_matrix
    
    if saveGraphs:
        # Create the correlation matrix
        corr_matrix = create_correlation_matrix(correlations, num_channels)

        # Plot the correlation matrix
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=False, fmt=".2f", cmap="coolwarm", square=True)
        plt.title('Correlation Matrix')
        plt.xlabel('Channel')
        plt.ylabel('Channel')
        plt.savefig('plots/python_PEs/xcorr_corr_matrix.png')

    return correlations


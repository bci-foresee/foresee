

# Other Promising Datasets

## Very interesting, worth a read

### [Laelaps: An Energy-Efficient Seizure Detection Algorithm from Long-term Human iEEG Recordings without False Alarms](https://www.research-collection.ethz.ch/handle/20.500.11850/349361)

- Good paper, available datasets, available code for algorithm. Built with hardware implementation in mind and also energy efficiency in mind.

- also home to The SWEC-ETHZ iEEG Database and Algorithms, which is used in a lot of studies (ie the next one)

- look at seizure detection pdf.



### [Hardware-Friendly Random Forest Classification of iEEG Signals for Implantable Seizure Detection](https://ieeexplore.ieee.org/document/10079382)

- The FPGA dynamic power consumption is 0.59 mW, paper for implantable seizure detection.

- uses a random forest classifier instead of SVM, slightly better performance with a much better latency.

- Algorithm designed for hardware efficiency.


## Just look at bullet points

### [Hardware Design of Real Time Epileptic Seizure Detection Based on STFT and SVM](https://ieeexplore.ieee.org/document/8467308)
- hardware level
- feature compressions (ie 64 nodes -> 23 inputs) gets rid of redundant info, less computation
- optimization of FFT block (multiple designs, HLS)
- however, EEG data not IEEG


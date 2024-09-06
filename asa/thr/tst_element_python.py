
import numpy as np
from pipelines.parent import Pipeline
from signals.parent import Window
from asa import SVM, FFT, THR, LOADER

# define the pipeline to test the fft PE
class THR_Pipe(Pipeline):

    def __init__(self, 
                 input_window: Window):
        
        # initialise the parent class
        super().__init__(input_window=input_window)

        # add processing elements to the pipeline
        self.loader = LOADER(input=input_window.load_signal(),
                      save_visualization=True)
        
        self.fft = FFT(n_samples=input_window.n_samples,
                       fs=input_window.fs,
                       clk=1,
                       berger_bands=[(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)],
                       save_visualization=True)

        
        # loading random weights, size= berger bands * channels
        
        random_weights = np.random.rand(len(self.fft.berger_bands) * input_window.n_channels)
        zero_weights = np.zeros(len(self.fft.berger_bands) * input_window.n_channels)
        one_weights = np.ones(len(self.fft.berger_bands) * input_window.n_channels)

        self.svm = SVM(weights=zero_weights,
                       save_visualization=False)
        
        self.thr = THR(lower_bound=0,
                       upper_bound=1,
                       save_visualization=False)
       
        # add PEs to list of elements
        self.add_elements([self.loader, self.fft, self.svm, self.thr])

        # define relationship between PEs
        self.add_edge(from_node=self.loader, to_node=self.fft)
        self.add_edge(from_node=self.fft, to_node=self.svm)
        self.add_edge(from_node=self.svm, to_node=self.thr)
    
    # run the end node of the pipeline, recursively running all the previous nodes
    def run(self):
        return self.thr.run()



def test_thr_basic() -> None:
    print()

    # input signal window
    # input signal window
    input_window = Window(fs=400, 
                          channels=2, 
                          samples=8000)
    
    input_window.generate_signal(frequencies=[10, 20, 40], 
                                 amplitudes=[20, 15, 10])

    # create test pipeline
    pipeline = THR_Pipe(input_window=input_window)
    
    output = pipeline.run()
    for element in pipeline.elements:
        print(f"Element: {element.name}, visualisation generated: {element.save_visualization}")
    print()
    print(f"output:\n {output}")
    assert output == 1, f"Expected 1 (all SVM weights = 0, therefore within threshold), but got {output}"

# lower_bound = 2
# upper_bound = 6

# thr = THR(lower_bound, upper_bound)

# value = 5
# result = thr.run(value)

# expected_result = 1
# assert result == expected_result, f"Expected {expected_result}, but got {result}"

# lower_bound = 3
# upper_bound = 4

# thr = THR(lower_bound, upper_bound)

# value = 2
# result = thr.run(value)

# expected_result = 0
# assert result == expected_result, f"Expected {expected_result}, but got {result}"
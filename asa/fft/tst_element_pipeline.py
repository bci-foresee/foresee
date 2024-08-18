from pipelines.parent import Pipeline
from signals.parent import Window
from asa import FFT, LOADER

# define the pipeline to test the fft PE
class FFT_Pipe(Pipeline):

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
       
        # add PEs to list of elements
        self.add_elements([self.loader, self.fft])

        # define relationship between PEs
        self.add_edge(from_node=self.loader, to_node=self.fft)
    
    # run the end node of the pipeline, recursively running all the previous nodes
    def run(self):
        return self.fft.run()
    

# run the pipeline to test the element
def test_fft_pipeline() -> None:

    # input signal window
    input_window = Window(fs=400, 
                          channels=2, 
                          samples=8000)
    
    input_window.generate_signal(frequencies=[10, 20, 40], 
                                 amplitudes=[20, 15, 10])

    # create test pipeline
    pipeline = FFT_Pipe(input_window=input_window)
    
    output_features = pipeline.run()
    for element in pipeline.elements:
        print(f"Element: {element.name}, visualisation generated: {element.save_visualization}")
    print()
    print(f"assert test case not implemented yet, output shape:\n {output_features.shape}")
    assert 1 == 1
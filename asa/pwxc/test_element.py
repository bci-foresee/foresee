from pipelines.parent import Pipeline
from signals.parent import Window
from asa import PWXC, LOADER

# define the pipeline to test the fft PE
class PWXC_Pipe(Pipeline):

    def __init__(self, 
                 input_window: Window):
        
        # initialise the parent class
        super().__init__(input_window=input_window)

        # add processing elements to the pipeline
        self.loader = LOADER(input=input_window.load_signal(),
                      save_vizualisation=True)
        
        self.pwxc = PWXC(window=input_window,
                         save_vizualisation=True)
       
        # add PEs to list of elements
        self.add_elements([self.loader, self.pwxc])

        # define relationship between PEs
        self.add_edge(from_node=self.loader, to_node=self.pwxc)
    
    # run the end node of the pipeline, recursively running all the previous nodes
    def run(self):
        return self.pwxc.run()
    

# run the pipeline to test the element
def test_pwxc_basic() -> None:

    # input signal window
    input_window = Window(fs=400, 
                          channels=4, 
                          samples=8000)
    
    input_window.generate_signal(frequencies=[10, 20, 40], 
                                 amplitudes=[20, 15, 10])

    # create test pipeline
    pipeline = PWXC_Pipe(input_window=input_window)
    
    output_features = pipeline.run()
    for element in pipeline.elements:
        print(f"Element: {element.name}, visualisation generated: {element.save_vizualisation}")
    print()
    print(f"assert test case not implemented yet, output shape:\n {output_features.shape}")
    assert 1 == 1
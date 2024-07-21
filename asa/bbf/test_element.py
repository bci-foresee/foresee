from pipelines.parent import Pipeline
from signals.parent import Window
from asa import BBF, LOADER

# define the pipeline to test the fft PE
class BBF_Pipe(Pipeline):

    def __init__(self, 
                 input_window: Window):
        
        # initialise the parent class
        super().__init__(input_window=input_window)

        # add processing elements to the pipeline
        self.loader = LOADER(input=input_window.load_signal(),
                      save_vizualisation=True)
        
        self.bbf = BBF(window=input_window,
                       berger_bands=[(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)],
                       save_vizualisation=True)
       
        # add PEs to list of elements
        self.add_elements([self.loader, self.bbf])

        # define relationship between PEs
        self.add_edge(from_node=self.loader, to_node=self.bbf)
    
    # run the end node of the pipeline, recursively running all the previous nodes
    def run(self):
        return self.bbf.run()
    

# run the pipeline to test the element
def test_bbf_basic() -> None:

    # input signal window
    input_window = Window(fs=400, 
                          channels=2, 
                          samples=8000)
    
    input_window.generate_signal(frequencies=[10, 20, 40], 
                                 amplitudes=[20, 15, 10])

    # create test pipeline
    pipeline = BBF_Pipe(input_window=input_window)
    
    output_features = pipeline.run()
    for element in pipeline.elements:
        print(f"Element: {element.name}, visualisation generated: {element.save_vizualisation}")
    print()
    print(f"assert test case not implemented yet, output shape:\n {output_features.shape}")
    assert 1 == 1
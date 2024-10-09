import sys
sys.path.append("./")

from app.static.processing_elements.fft.fft import FFT
from app.static.processing_elements.svm.svm import SVM
from app.static.processing_elements.thr.thr import THR
from app.static.processing_elements.bbf.bbf import BBF
from app.static.processing_elements.pwxc.pwxc import PWXC
from app.static.processing_elements.loader.loader import LOADER
from app.static.pipelines.pipeline import Pipeline
import numpy as np
from signals.parent import Window
from asa import SVM, FFT, THR, LOADER

# define the pipeline to test the fft PE
class Shiao_Pipe(Pipeline):

    name = "Seizure Shiao"

    def __init__(self, input_window: Window):

        # initialise the parent class
        super().__init__(input_window=input_window)

        berger_bands = [(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80),
                        (80, 180)]

        # add processing elements to the pipeline
        self.loader = LOADER(input=input_window.load_signal(),
                             save_visualization=True)

        self.fft = FFT(n_samples=input_window.n_samples,
                       fs=input_window.fs,
                       clk=1,
                       berger_bands=berger_bands,
                       save_visualization=True)

        self.bbf = BBF(fs=input_window.fs,
                       berger_bands=berger_bands,
                       save_visualization=True)

        self.pwxc = PWXC(n_channels=input_window.n_channels,
                         save_visualization=True)

        # loading random weights, size = berger bands * channels + berger bands * channels + (channels * (channels - 1)) / 2

        weights_size = int(
            (len(berger_bands) * input_window.n_channels +
             len(berger_bands) * input_window.n_channels +
             (input_window.n_channels * (input_window.n_channels - 1)) / 2))

        print(f"weights_size: {weights_size}")

        random_weights = np.random.rand(weights_size)
        zero_weights = np.zeros(weights_size)
        one_weights = np.ones(weights_size)

        self.svm = SVM(weights=zero_weights, save_visualization=False)

        self.thr = THR(lower_bound=0, upper_bound=1, save_visualization=False)

        # add PEs to list of elements
        self.add_elements(
            [self.loader, self.fft, self.bbf, self.pwxc, self.svm, self.thr])

        # define relationship between PEs
        self.add_edge(from_node=self.loader, to_node=self.fft)
        self.add_edge(from_node=self.loader, to_node=self.bbf)
        self.add_edge(from_node=self.loader, to_node=self.pwxc)

        self.add_edge(from_node=self.fft, to_node=self.svm)
        self.add_edge(from_node=self.bbf, to_node=self.svm)
        self.add_edge(from_node=self.pwxc, to_node=self.svm)

        self.add_edge(from_node=self.svm, to_node=self.thr)

    # run the end node of the pipeline, recursively running all the previous nodes
    def run(self):
        return self.thr.run()

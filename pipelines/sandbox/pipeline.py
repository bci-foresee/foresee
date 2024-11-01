# from pipelines.parent import Pipeline
# from signals.parent import Window
# from asa import FFT, LOADER
# import numpy as np
# from numpy.typing import NDArray
# import matplotlib.pyplot as plt

# class Sandbox_Pipe(Pipeline):

#     def __init__(self, input_window: Window):

#         super().__init__(input_window=input_window)

#         self.loader = LOADER(input=input_window.load_signal(),
#                              save_visualization=True)

#         self.fft = FFT(n_samples=input_window.n_samples,
#                        fs=input_window.fs,
#                        clk=1,
#                        berger_bands=[(0.1, 4), (4, 8), (8, 12), (12, 30),
#                                      (30, 80), (80, 180)],
#                        save_visualization=True)

#         self.add_elements([self.loader, self.fft])

#         self.add_edge(from_node=self.loader, to_node=self.fft)

#     def run(self):
#         return self.fft.run()

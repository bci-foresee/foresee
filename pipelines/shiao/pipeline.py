
from pipelines import Pipeline
from asa import FFT, SVM, THR, BBF, PWXC


class Shiao(Pipeline):

    BERGER_BANDS = [(0.1, 4), (4, 8), (8, 12), (12, 30), (30, 80), (80, 180)]

    def __init__(self):
        self.fft = FFT(1024)
        self.svm = SVM([])
        self.thr = THR(1, 2)
        self.bbf = BBF()
        self.pwxc = PWXC()

        self.add_elements([self.fft, self.svm, self.thr, self.bbf, self.pwxc])

        self.add_edge(self.fft, self.svm)
        self.add_edge(self.bbf, self.svm)
        self.add_edge(self.pwxc, self.svm)
        self.add_edge(self.svm, self.thr)

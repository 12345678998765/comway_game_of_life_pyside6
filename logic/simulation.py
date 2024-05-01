from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QLabel

from logic.constants import FPS


class SimulationThread(QThread):
    sig = Signal(QLabel)

    def __init__(self, show_gens_label: QLabel):
        super().__init__()
        self.flag = True
        self.fps = FPS
        self.show_gens_label = show_gens_label

    def run(self):
        self.flag = True
        while self.flag:
            self.sig.emit(self.show_gens_label)
            self.msleep((1000 // self.fps))

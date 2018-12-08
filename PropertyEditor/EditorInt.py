from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtCore import pyqtSignal

class EditorInt(QSpinBox):
    dataChanged = pyqtSignal(int)

    def __init__(self, value, spinBoxWidth):
        super().__init__()

        self.setFixedWidth(spinBoxWidth)
        self.setRange(-100000,100000)
        self.setValue(value)

        self.valueChanged.connect(self._dataChanged)

    def _dataChanged(self, newVal):
        self.dataChanged.emit(newVal)

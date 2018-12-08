from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtCore import pyqtSignal

class EditorFloat(QDoubleSpinBox):
    dataChanged = pyqtSignal(float)

    def __init__(self, value, spinBoxWidth):
        super().__init__()

        self.setFixedWidth(spinBoxWidth)
        self.setValue(value)

        self.valueChanged.connect(self._dataChanged)

    def _dataChanged(self, newVal):
        self.dataChanged.emit(newVal)

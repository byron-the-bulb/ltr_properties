from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtCore import pyqtSignal

class EditorFloat(QDoubleSpinBox):
    dataChanged = pyqtSignal(float)

    def __init__(self, editorGenerator, value, name):
        super().__init__()

        self.setFixedWidth(editorGenerator.getSpinBoxWidth())
        self.setRange(-100000,100000)
        self.setValue(value)

        self.valueChanged.connect(self._dataChanged)

    def _dataChanged(self, newVal):
        self.dataChanged.emit(newVal)

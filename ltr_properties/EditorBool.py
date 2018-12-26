from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import pyqtSignal

class EditorBool(QCheckBox):
    dataChanged = pyqtSignal(bool)

    def __init__(self, editorGenerator, value, name):
        super().__init__()

        self.setCheckState(2 if value else 0)

        self.stateChanged.connect(self._dataChanged)

    def _dataChanged(self, newVal):
        boolValue = True if newVal > 0 else False
        self.dataChanged.emit(boolValue)

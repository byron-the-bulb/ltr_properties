from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSignal

class EditorString(QLineEdit):
    dataChanged = pyqtSignal(str)

    def __init__(self, value):
        super().__init__()

        self.setText(value)

        self.editingFinished.connect(self._dataChanged)

    def _dataChanged(self):
        self.dataChanged.emit(self.text())

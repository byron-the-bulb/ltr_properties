from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSignal

class EditorString(QLineEdit):
    dataChanged = pyqtSignal(str)

    def __init__(self, editorGenerator, value, name):
        super().__init__()

        self.setText(value)

        self._oldValue = value

        self.editingFinished.connect(self._dataChanged)

    def _dataChanged(self):
        if self._oldValue != self.text():
            self.dataChanged.emit(self.text())
            self._oldValue = self.text()

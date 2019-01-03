from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSignal

class EditorString(QLineEdit):
    dataChanged = pyqtSignal(str)

    def __init__(self, editorGenerator, targetObject, name, typeHint):
        super().__init__()
        self._editorGenerator = editorGenerator

        self.setText(targetObject)

        self._oldValue = targetObject

        self.editingFinished.connect(self._dataChanged)

    def _dataChanged(self):
        if self._oldValue != self.text():
            with self._editorGenerator.threadLock():
                self.dataChanged.emit(self.text())
                self._oldValue = self.text()

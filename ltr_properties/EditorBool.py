from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import pyqtSignal

class EditorBool(QCheckBox):
    dataChanged = pyqtSignal(bool)

    def __init__(self, editorGenerator, targetObject, name, typeHint):
        super().__init__()
        self._editorGenerator = editorGenerator

        self.setCheckState(2 if targetObject else 0)

        self.stateChanged.connect(self._dataChanged)

    def _dataChanged(self, newVal):
        with self._editorGenerator.threadLock():
            boolValue = True if newVal > 0 else False
            self.dataChanged.emit(boolValue)

from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtCore import pyqtSignal

class EditorInt(QSpinBox):
    dataChanged = pyqtSignal(int)

    def __init__(self, editorGenerator, targetObject, name, typeHint):
        super().__init__()
        self._editorGenerator = editorGenerator

        self.setFixedWidth(editorGenerator.spinBoxWidth())
        self.setRange(-100000,100000)
        self.setValue(targetObject)

        self.valueChanged.connect(self._dataChanged)

    def _dataChanged(self, newVal):
        with self._editorGenerator.threadLock():
            self.dataChanged.emit(newVal)

from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import pyqtSignal

from enum import Enum

class EditorEnum(QComboBox):
    dataChanged = pyqtSignal(Enum)

    def __init__(self, editorGenerator, targetObject, name, typeHint):
        super().__init__()
        self._editorGenerator = editorGenerator

        self._enumType = type(targetObject)

        for enumValue in self._enumType:
            self.addItem(enumValue.name)
        self.setCurrentText(targetObject.name)

        self.currentTextChanged.connect(self._dataChanged)

    def _dataChanged(self, newVal):
        with self._editorGenerator.threadLock():
            self.dataChanged.emit(self._enumType[newVal])

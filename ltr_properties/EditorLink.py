from .Link import Link
from . import TypeUtils

from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QHBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal

import os

class EditorLink(QWidget):
    dataChanged = pyqtSignal(int)

    def __init__(self, editorGenerator, targetObject:Link, name, typeHint):
        super().__init__()

        layout = QHBoxLayout(self)

        self._editorGenerator = editorGenerator
        self._targetObject = targetObject
        self._name = name
        self._typeHint = typeHint

        self._label = QLabel(targetObject.filename)
        layout.addWidget(self._label)
        self._button = QPushButton("Browse")
        layout.addWidget(self._button)

        self._button.clicked.connect(self._chooseFile)

    def _chooseFile(self):
        rootPath = self._editorGenerator.serializer().root()
        filename = QFileDialog.getOpenFileName(self, self._name, rootPath, "*.json")
        if filename[0]:
            newPath = os.path.relpath(filename[0], rootPath)
            obj = self._editorGenerator.serializer().load(newPath)
            
            try:
                TypeUtils.checkType(obj, TypeUtils.getLinkTypeHint(self._typeHint), self._name)
            except TypeError as ex:
                QMessageBox.warning(self, "Type Error", str(ex))
            else:
                with self._editorGenerator.threadLock():
                    self._targetObject.setObject(obj)
                    self.dataChanged.emit(self._targetObject)
                    self._label.setText(newPath)

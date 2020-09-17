from .Link import Link
from .Icons import Icons
from . import TypeUtils

from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QHBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal

import os

class EditorLink(QWidget):
    dataChanged = pyqtSignal(Link)

    def __init__(self, editorGenerator, targetObject:Link, name, typeHint):
        super().__init__()

        layout = QHBoxLayout(self)

        self._editorGenerator = editorGenerator
        self._targetObject = targetObject
        self._name = name
        self._typeHint = typeHint

        self._label = QLabel(targetObject.filename)
        layout.addWidget(self._label)

        self._openButton = self._editorGenerator.createButton(Icons.Open)
        self._openButton.clicked.connect(self._onChooseFileClicked)
        layout.addWidget(self._openButton)

        self._deleteButton = self._editorGenerator.createButton(Icons.Delete)
        self._deleteButton.clicked.connect(self._delete)
        layout.addWidget(self._deleteButton)

        self._gotoButton = self._editorGenerator.createButton(Icons.Goto)
        self._gotoButton.clicked.connect(self._goto)
        layout.addWidget(self._gotoButton)

    def _chooseFile(self):
        rootPath = self._editorGenerator.serializer().root()
        filename = QFileDialog.getOpenFileName(self, self._name, rootPath, "*.json")
        if filename[0]:
            newPath = os.path.relpath(filename[0], rootPath)
            if ".." in newPath:
                QMessageBox.warning(self, "Invalid Path", os.path.abspath(newPath) + "\n\nis outside the root path\n\n" + os.path.abspath(rootPath))
                return None

            return newPath

        return None

    def _onChooseFileClicked(self):
        newPath = self._chooseFile()
        if newPath != None:
            obj = self._editorGenerator.serializer().load(newPath)
            
            try:
                TypeUtils.checkType(obj, TypeUtils.getLinkTypeHint(self._typeHint), self._name)
            except TypeError as ex:
                QMessageBox.warning(self, "Type Error", str(ex))
            else:
                with self._editorGenerator.threadLock():
                    self._targetObject.setObject(newPath, obj)
                    self.dataChanged.emit(self._targetObject)
                    self._label.setText(newPath)

    def _goto(self):
        target = self._label.text()
        self._editorGenerator.gotoObject.emit(target)

    def _delete(self):
        with self._editorGenerator.threadLock():
            self._targetObject.setObject("", None)
            self.dataChanged.emit(self._targetObject)
            self._label.setText("")

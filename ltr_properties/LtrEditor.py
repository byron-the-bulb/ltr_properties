from .ObjectTree import ObjectTree
from .PropertyEditorWidget import PropertyEditorWidget
from .Serializer import Serializer

import threading
import os

from PyQt5.QtWidgets import QWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QScrollArea

class LtrEditor(QWidget):
    def __init__(self, root, module, threadLock=threading.Lock(), parent=None):
        super().__init__(parent)

        self._threadLock = threadLock

        self._serializer = Serializer(root, module)

        mainLayout = QHBoxLayout(self)

        self._objectTree = ObjectTree(root)
        sizePolicy = self._objectTree.sizePolicy()
        sizePolicy.setHorizontalStretch(1)
        self._objectTree.setSizePolicy(sizePolicy)
        mainLayout.addWidget(self._objectTree)

        self._objectTree.fileActivated.connect(self._fileActivated)

        self._tabWidget = QTabWidget()
        sizePolicy = self._tabWidget.sizePolicy()
        sizePolicy.setHorizontalStretch(2)
        self._tabWidget.setSizePolicy(sizePolicy)
        mainLayout.addWidget(self._tabWidget)

        self._customEditorMappings = {}
        self._tabPaths = []

    def addTargetObject(self, obj, name, path, dataChangeCallback=None):
        scrollArea = QScrollArea()

        pe = PropertyEditorWidget(self._serializer)
        pe.setThreadLock(self._threadLock)
        for objType, editType in self._customEditorMappings.items():
            pe.registerCustomEditor(objType, editType)
        pe.setTargetObject(obj)

        pe.editorGenerator().gotoObject.connect(self._onGotoObject)

        scrollArea.setWidget(pe)

        if dataChangeCallback:
            pe.dataChanged.connect(dataChangeCallback)

        scrollArea.path = path

        self._tabWidget.addTab(scrollArea, name)
        self._tabPaths.append(path)

    def addCustomEditorMapping(self, objType, editorType):
        self._customEditorMappings[objType] = editorType

    def customEditorMappings(self):
        return self._customEditorMappings

    def objectTree(self):
        return self._objectTree

    def threadLock(self):
        return self._threadLock

    def _onGotoObject(self, path):
        name = os.path.basename(path).replace(".json", "")
        self._fileActivated(name, path)

    def _fileActivated(self, name, path):
        path = os.path.abspath(path)
        obj = self._serializer.load(path)
        for tabIndex in range(self._tabWidget.count()):
            if self._tabPaths[tabIndex] == path:
                self._tabWidget.setCurrentIndex(tabIndex)
                return

        self.addTargetObject(obj, name, path)
        self._tabWidget.setCurrentIndex(self._tabWidget.count() - 1)

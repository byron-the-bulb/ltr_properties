from .ObjectTree import ObjectTree
from .PropertyEditorWidget import PropertyEditorWidget

import threading

from PyQt5.QtWidgets import QWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QScrollArea

class LtrEditor(QWidget):
    def __init__(self, root, threadLock=threading.Lock(), parent=None):
        super().__init__(parent)

        self._threadLock = threadLock

        mainLayout = QHBoxLayout(self)

        self._objectTree = ObjectTree(root)
        sizePolicy = self._objectTree.sizePolicy()
        sizePolicy.setHorizontalStretch(1)
        self._objectTree.setSizePolicy(sizePolicy)
        mainLayout.addWidget(self._objectTree)

        self._tabWidget = QTabWidget()
        sizePolicy = self._tabWidget.sizePolicy()
        sizePolicy.setHorizontalStretch(2)
        self._tabWidget.setSizePolicy(sizePolicy)
        mainLayout.addWidget(self._tabWidget)

        self._customEditorMappings = {}

    def addTargetObject(self, obj, name, dataChangeCallback=None):
        scrollArea = QScrollArea()

        pe = PropertyEditorWidget()
        pe.setThreadLock(self._threadLock)
        for objType, editType in self._customEditorMappings.items():
            pe.registerCustomEditor(objType, editType)
        pe.setTargetObject(obj)

        scrollArea.setWidget(pe)

        if dataChangeCallback:
            pe.dataChanged.connect(dataChangeCallback)

        self._tabWidget.addTab(scrollArea, name)

    def addCustomEditorMapping(self, objType, editorType):
        self._customEditorMappings[objType] = editorType

    def customEditorMappings(self):
        return self._customEditorMappings

    def objectTree(self):
        return self._objectTree

    def threadLock(self):
        return self._threadLock

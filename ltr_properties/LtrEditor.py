from .ObjectTree import ObjectTree
from .Icons import Icons
from .PropertyEditorWidget import PropertyEditorWidget
from .Serializer import Serializer

import threading
import os

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QScrollArea, QShortcut, QPushButton
from PyQt5.QtGui import QKeySequence

class LtrEditor(QWidget):
    def __init__(self, root, module, threadLock=threading.Lock(), parent=None):
        super().__init__(parent)

        # Make sure icons are loaded before we use them.
        Icons.LoadIcons()

        self._threadLock = threadLock

        self._serializer = Serializer(root, module)

        mainLayout = QHBoxLayout(self)

        self._objectTree = ObjectTree(root)
        sizePolicy = self._objectTree.sizePolicy()
        sizePolicy.setHorizontalStretch(1)
        self._objectTree.setSizePolicy(sizePolicy)
        self._objectTree.fileActivated.connect(self._openFile)
        mainLayout.addWidget(self._objectTree)

        rightPanel = QWidget()
        sizePolicy = rightPanel.sizePolicy()
        sizePolicy.setHorizontalStretch(2)
        rightPanel.setSizePolicy(sizePolicy)
        mainLayout.addWidget(rightPanel)

        rightLayout = QVBoxLayout(rightPanel)
        rightLayout.setContentsMargins(0, 0, 0, 0)

        buttonWidget = QWidget()
        self._buttonLayout = QHBoxLayout(buttonWidget)
        self._buttonLayout.setContentsMargins(0, 0, 0, 0)
        rightLayout.addWidget(buttonWidget)

        self._saveButton = QPushButton(Icons.Save, "")
        self._saveButton.clicked.connect(self._onSaveClicked)
        self._saveButton.setFixedSize(24, 24)
        self._saveButton.setIconSize(QSize(24, 24))
        self._buttonLayout.addWidget(self._saveButton)

        self._revertButton = QPushButton(Icons.Revert, "")
        self._revertButton.clicked.connect(self._onRevertClicked)
        self._revertButton.setFixedSize(24, 24)
        self._revertButton.setIconSize(QSize(24, 24))
        self._buttonLayout.addWidget(self._revertButton)

        self._buttonLayout.addStretch()

        self._tabWidget = QTabWidget()
        self._tabWidget.setTabsClosable(True)
        self._tabWidget.tabCloseRequested.connect(self._onTabCloseRequested)
        self._closeTabShortcut = QShortcut(QKeySequence("Ctrl+W"), self, self._onCloseCurrentTab)
        rightLayout.addWidget(self._tabWidget)

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
        self._openFile(name, path)

    def _onCloseCurrentTab(self):
        if self._tabWidget.count() > 0: 
            self._onTabCloseRequested(self._tabWidget.currentIndex())

    def _onRevertClicked(self):
        if self._tabWidget.currentIndex() >= 0:
            path = self._tabPaths[self._tabWidget.currentIndex()]
            targetObject = self._serializer.load(path)
            self._tabWidget.currentWidget().widget().setTargetObject(targetObject)

    def _onSaveClicked(self):
        if self._tabWidget.currentIndex() >= 0:
            path = self._tabPaths[self._tabWidget.currentIndex()]
            targetObject = self._tabWidget.currentWidget().widget().targetObject()
            self._serializer.save(path, targetObject)

    def _onTabCloseRequested(self, index):
        self._tabWidget.removeTab(index)
        del self._tabPaths[index]

    def _openFile(self, name, path):
        path = os.path.abspath(path)
        obj = self._serializer.load(path)
        for tabIndex in range(self._tabWidget.count()):
            if self._tabPaths[tabIndex] == path:
                self._tabWidget.setCurrentIndex(tabIndex)
                return

        self.addTargetObject(obj, name, path)
        self._tabWidget.setCurrentIndex(self._tabWidget.count() - 1)
        self._tabWidget.setFocus()

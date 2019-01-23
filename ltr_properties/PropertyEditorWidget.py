from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

from .Icons import Icons

from .EditorGenerator import EditorGenerator

from .UIUtils import clearLayout

import threading

class PropertyEditorWidget(QWidget):
    dataChanged = pyqtSignal()

    def __init__(self, serializer, targetObject=None, labelWidth=100, spinBoxWidth=70, customEditors={}):
        super().__init__()

        # Make sure icons are loaded before we use them.
        Icons.LoadIcons()

        self._serializer = serializer
        
        self._labelWidth = labelWidth
        self._spinBoxWidth = spinBoxWidth

        self._targetObject = targetObject

        self._customEditors = customEditors

        self._threadLock = threading.Lock()
           
        QVBoxLayout(self)
        self.layout().setContentsMargins(0, 0, 0, 0)

    #TODO: This feels pretty gross.
    def editorGenerator(self):
        return self._editorGenerator

    def labelWidth(self):
        return self._labelWidth

    def registerCustomEditor(self, classObj, editorClass):
        self._customEditors[classObj] = editorClass
        self._initUI()

    def setLabelWidth(self, width):
        self._labelWidth = width
        self._initUI()

    def setTargetObject(self, target):
        self._targetObject = target
        self._initUI()

    def setSpinBoxWidth(self, width):
        self._spinBoxWidth = width
        self._initUI()

    def setThreadLock(self, threadLock):
        self._threadLock = threadLock
        self._initUI()

    def spinBoxWidth(self):
        return self._spinBoxWidth

    def targetObject(self):
        return self._targetObject

    def threadLock(self):
        return self._threadLock
        
    def _dataChanged(self):
        self.dataChanged.emit()
        
    def _initUI(self):
        clearLayout(self.layout())

        if self._targetObject:
            self._editorGenerator = EditorGenerator(self._customEditors, self._labelWidth, self._spinBoxWidth, self._threadLock, self._serializer)
            editor = self._editorGenerator.createWidget(self._targetObject)
            if hasattr(editor, "dataChanged"):
                editor.dataChanged.connect(self._dataChanged)
            self.layout().addWidget(editor)

            self.layout().addStretch()

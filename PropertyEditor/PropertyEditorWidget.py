from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

from .EditorGenerator import EditorGenerator

def clearLayout(layout):
    for i in reversed(range(layout.count())): 
        layout.itemAt(i).widget().setParent(None)

class PropertyEditorWidget(QWidget):
    dataChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        self._labelWidth = 100
        self._spinBoxWidth = 70

        self._targetObject = None

        self._customEditors = {}
           
        QVBoxLayout(self)
        self.layout().setContentsMargins(0, 0, 0, 0)

    def labelWidth(self):
        return self._labelWidth

    def registerCustomEditor(self, classObj, editorClass):
        self._customEditors[classObj] = editorClass

    def setLabelWidth(self, width):
        self._labelWidth = width
        self._initUI()

    def setTargetObject(self, target):
        self._targetObject = target
        self._initUI()

    def setSpinBoxWidth(self, width):
        self._spinBoxWidth = width
        self._initUI()

    def spinBoxWidth(self):
        return self._spinBoxWidth

    def targetObject(self):
        return self._targetObject
        
    def _dataChanged(self):
        self.dataChanged.emit()
        
    def _initUI(self):
        clearLayout(self.layout())

        if self._targetObject:
            editorGenerator = EditorGenerator(self._customEditors, self._labelWidth, self._spinBoxWidth)
            editor = editorGenerator.createWidget(self._targetObject)
            editor.dataChanged.connect(self._dataChanged)
            self.layout().addWidget(editor)

            self.layout().addStretch()

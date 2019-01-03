from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

from .Icons import Icons

from .EditorGenerator import EditorGenerator

from .UIUtils import clearLayout

class PropertyEditorWidget(QWidget):
    dataChanged = pyqtSignal()

    #TODO: Do this in a less hacky way
    threadLock = None

    def __init__(self):
        Icons.LoadIcons()

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
            if hasattr(editor, "dataChanged"):
                editor.dataChanged.connect(self._dataChanged)
            self.layout().addWidget(editor)

            self.layout().addStretch()

from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal

from .EditorHeader import EditorHeader
from .Icons import Icons
from .UIUtils import clearLayout

class CompoundEditor(QWidget):
    dataChanged = pyqtSignal(object)
    shouldSkipLabel = True
    isHorizontalLayout = False
    canDeleteElements = False

    def __init__(self, editorGenerator, targetObject, name):
        super().__init__()

        self._editorGenerator = editorGenerator
        self._targetObject = targetObject

        self._widgetLayout = self._createLayout(name)
        
        self._createWidgetsForObject()

    # Should yield name, value, setter for each property.
    def _getProperties(self):
        raise NotImplementedError()

    def _deleteClicked(self, name):
        raise NotImplementedError()

    def _getHeaderWidgets(self):
        return []

    def _createWidgetsForObject(self):
        # Make sure we can call this multiple times
        clearLayout(self._widgetLayout)
        for name, value, setter in self._getProperties():
            editor = self._editorGenerator.createWidget(value, name, setter)
            editor.dataChanged.connect(self._dataChanged)

            self._addEditorToLayout(name, editor)

    def _dataChanged(self):
        if hasattr(self._targetObject, "onDataEdited"):
            self._targetObject.onDataEdited()
        self.dataChanged.emit(self._targetObject)

    def _createLayout(self, name):
        selfLayout = QVBoxLayout(self)
        selfLayout.setContentsMargins(0, 0, 0, 0)
        selfLayout.setSpacing(0)

        frame = QFrame()
        if name:
            header = EditorHeader(name, frame, self._editorGenerator, self._getHeaderWidgets())
            selfLayout.addWidget(header)
        selfLayout.addWidget(frame)

        if self.isHorizontalLayout:
            layout = QHBoxLayout(frame)
            return layout
        else:
            layout = QVBoxLayout(frame)
            return layout

    def _addEditorToLayout(self, name, editor):
        deleteButton = None
        if self.canDeleteElements:
            deleteButton = self._editorGenerator.createButton(Icons.Delete)
            deleteButton.clicked.connect(lambda: self._deleteClicked(name))
            
        if hasattr(editor, "shouldSkipLabel") and editor.shouldSkipLabel:
            if deleteButton:
                self._widgetLayout.addWidget(self._editorGenerator.wrapWidget("", editor, deleteButton))
            else:
                self._widgetLayout.addWidget(editor)
        elif self.isHorizontalLayout:
            if deleteButton:
                self._widgetLayout.addWidget(deleteButton)
            self._widgetLayout.addWidget(QLabel(name))
            self._widgetLayout.addWidget(editor)
        else:
            self._widgetLayout.addWidget(self._editorGenerator.wrapWidget(name, editor, deleteButton))

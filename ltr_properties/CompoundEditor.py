from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal

from .EditorHeader import EditorHeader
from .HoverableButton import HoverableButton
from .Icons import Icons
from .UIUtils import clearLayout

class CompoundEditor(QWidget):
    dataChanged = pyqtSignal(object)
    shouldSkipLabel = True
    isHorizontalLayout = False
    canDeleteElements = False

    def __init__(self, editorGenerator, targetObject, name):
        super().__init__()

        self._widgetLayout = self._createLayout(name, editorGenerator.preLabelWidth())
        self._editorGenerator = editorGenerator
        self._targetObject = targetObject
        
        self._createWidgetsForObject()

    # Should yield name, value, setter for each property.
    def _getProperties(self):
        raise NotImplementedError()

    def _deleteClicked(self, name):
        raise NotImplementedError()

    def _createWidgetsForObject(self):
        # Make sure we can call this multiple times
        clearLayout(self._widgetLayout)
        for name, value, setter in self._getProperties():
            editor = self._editorGenerator.createWidget(value, name, setter)
            editor.dataChanged.connect(self._dataChanged)

            self._addEditorToLayout(self._editorGenerator, self._widgetLayout, name, editor)

    def _dataChanged(self):
        if hasattr(self._targetObject, "onDataEdited"):
            self._targetObject.onDataEdited()
        self.dataChanged.emit(self._targetObject)

    def _createLayout(self, name, preLabelWidth):
        selfLayout = QVBoxLayout(self)
        selfLayout.setContentsMargins(0, 0, 0, 0)
        selfLayout.setSpacing(0)

        frame = QFrame()
        if name:
            header = EditorHeader(name, frame, preLabelWidth)
            selfLayout.addWidget(header)
        selfLayout.addWidget(frame)

        if self.isHorizontalLayout:
            layout = QHBoxLayout(frame)
            return layout
        else:
            layout = QVBoxLayout(frame)
            return layout

    def _addEditorToLayout(self, editorGenerator, boxLayout, name, editor):
        if hasattr(editor, "shouldSkipLabel") and editor.shouldSkipLabel:
            boxLayout.addWidget(editor)
        elif self.isHorizontalLayout:
            boxLayout.addWidget(QLabel(name))
            boxLayout.addWidget(editor)
        else:
            preLabelWidget = None
            if self.canDeleteElements:
                preLabelWidget = HoverableButton(Icons.Delete, "")
                preLabelWidget.clicked.connect(lambda: self._deleteClicked(name))
            boxLayout.addWidget(editorGenerator.wrapWidgetWithLabel(name, editor, preLabelWidget))

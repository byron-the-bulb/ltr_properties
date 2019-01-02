from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

from .EditorHeader import EditorHeader

class CompoundEditor(QWidget):
    dataChanged = pyqtSignal(object)
    shouldSkipLabel = True
    isHorizontalLayout = False

    def __init__(self, editorGenerator, targetObject, name):
        super().__init__()

        layout = self._createLayout(name)

        self._targetObject = targetObject
        
        self._createWidgetsForObject(layout, editorGenerator, targetObject)

    # Should yield name, value, setter for each property.
    def _getProperties(self, targetObject):
        raise NotImplementedError()

    def _createWidgetsForObject(self, boxLayout, editorGenerator, targetObject):
        for name, value, setter in self._getProperties(targetObject):
            editor = editorGenerator.createWidget(value, name, setter)
            editor.dataChanged.connect(self._dataChanged)

            self._addEditorToLayout(editorGenerator, boxLayout, name, editor)

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
            header = EditorHeader(name, frame)
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
            boxLayout.addWidget(editorGenerator.wrapWidgetWithLabel(name, editor))

from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal

import typing

from .EditorHeader import EditorHeader
from .Icons import Icons
from .UIUtils import clearLayout

class CompoundEditor(QWidget):
    dataChanged = pyqtSignal(object)
    shouldSkipLabel = True
    isHorizontalLayout = False
    canDeleteElements = False
    canMoveElements = False

    def __init__(self, editorGenerator, targetObject, name, typeHint):
        super().__init__()

        self._editorGenerator = editorGenerator
        self._targetObject = targetObject
        self._typeHint = typeHint

        self._widgetLayout = self._createLayout(name)

        self._childWidgetMap = {}
        
        self._createWidgetsForObject()

    def childWidget(self, path):
        return self._childWidgetMap[path] if path in self._childWidgetMap else None

    # Should yield name, value, setter, typeHint for each property.
    def _getProperties(self):
        raise NotImplementedError()

    def _deleteClicked(self, name):
        raise NotImplementedError()

    def _getHeaderWidgets(self):
        return []

    def _createWidgetsForObject(self):
        # Make sure we can call this multiple times
        clearLayout(self._widgetLayout)

        for name, value, setter, typeHint in self._getProperties():
            editor = self._editorGenerator.createWidget(value, name, setter, typeHint=typeHint)

            self._childWidgetMap[name] = editor

            if hasattr(editor, "dataChanged"):
                editor.dataChanged.connect(self._dataChanged)

            self._addEditorToLayout(name, editor)

        if self.isHorizontalLayout:
            self._widgetLayout.addStretch()

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
        preLabelWidget = None
        if self.canDeleteElements or self.canMoveElements:
            preLabelWidget = QWidget()
            preLabelLayout = QHBoxLayout(preLabelWidget)
            preLabelLayout.setContentsMargins(0, 0, 0, 0)
            preLabelLayout.setSpacing(0)

        if self.canDeleteElements:
            deleteButton = self._editorGenerator.createButton(Icons.Delete)
            deleteButton.clicked.connect(lambda: self._deleteClicked(name))
            preLabelWidget.layout().addWidget(deleteButton)

        if self.canMoveElements:
            moveWidget = QWidget()
            moveLayout = QVBoxLayout(moveWidget)
            moveLayout.setContentsMargins(0, 0, 0, 0)
            moveLayout.setSpacing(0)
            preLabelWidget.layout().addWidget(moveWidget)
            moveButtonUp = self._editorGenerator.createButton(Icons.ArrowUp)
            moveButtonDown = self._editorGenerator.createButton(Icons.ArrowDown)
            moveButtonUp.clicked.connect(lambda: self._moveClicked(name, -1))
            moveButtonDown.clicked.connect(lambda: self._moveClicked(name, 1))
            moveLayout.addWidget(moveButtonUp)
            moveLayout.addWidget(moveButtonDown)
            
        if hasattr(editor, "shouldSkipLabel") and editor.shouldSkipLabel:
            if preLabelWidget:
                self._widgetLayout.addWidget(self._editorGenerator.wrapWidget("", editor, preLabelWidget))
            else:
                self._widgetLayout.addWidget(editor)
        elif self.isHorizontalLayout:
            if preLabelWidget:
                self._widgetLayout.addWidget(preLabelWidget)
            self._widgetLayout.addWidget(QLabel(name))
            self._widgetLayout.addWidget(editor)
        else:
            self._widgetLayout.addWidget(self._editorGenerator.wrapWidget(name, editor, preLabelWidget))

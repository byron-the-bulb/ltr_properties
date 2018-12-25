from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

class __EditorSlottedClassBase(QWidget):
    dataChanged = pyqtSignal(object)
    shouldSkipLabel = True

    def __init__(self, editorGenerator, targetObject, name):
        super().__init__()

        layout = self._createLayout(name)

        self._targetObject = targetObject
        
        self._createWidgetsForObject(layout, editorGenerator, targetObject)

    def _createWidgetsForObject(self, boxLayout, editorGenerator, targetObject):
        for name in targetObject.__slots__:
            # Let users add hidden properties (including __dict__).
            if name.startswith("_"):
                continue
                
            setter = lambda val, thisName=name: setattr(targetObject, thisName, val)
            
            editor = editorGenerator.createWidget(getattr(targetObject, name), name, setter)
            editor.dataChanged.connect(self._dataChanged)

            self._addEditorToLayout(editorGenerator, boxLayout, name, editor)
            
    def _dataChanged(self):
        if hasattr(self._targetObject, "onDataEdited"):
            self._targetObject.onDataEdited()
        self.dataChanged.emit(self._targetObject)

class EditorSlottedClass(__EditorSlottedClassBase):
    def __init__(self, editorGenerator, targetObject, name):
        super().__init__(editorGenerator, targetObject, name)

    def _createLayout(self, name):
        if (name):
            selfLayout = QVBoxLayout(self)
            selfLayout.setContentsMargins(0, 0, 0, 0)
            box = QGroupBox(name)
            selfLayout.addWidget(box)
            layout = QVBoxLayout(box)
        else:
            layout = QVBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        return layout

    def _addEditorToLayout(self, editorGenerator, boxLayout, name, editor):
        if hasattr(editor, "shouldSkipLabel") and editor.shouldSkipLabel:
            boxLayout.addWidget(editor)
        else:
            boxLayout.addWidget(editorGenerator.wrapWidgetWithLabel(name, editor))

class EditorSlottedClassHorizontal(__EditorSlottedClassBase):
    def __init__(self, editorGenerator, targetObject, name):
        super().__init__(editorGenerator, targetObject, name)

    def _createLayout(self, name):
        selfLayout = QVBoxLayout(self)
        box = QGroupBox(name)
        selfLayout.addWidget(box)
        layout = QHBoxLayout(box)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        return layout

    def _addEditorToLayout(self, editorGenerator, boxLayout, name, editor):
        if hasattr(editor, "shouldSkipLabel") and editor.shouldSkipLabel:
            boxLayout.addWidget(editor)
        else:
            boxLayout.addWidget(QLabel(name))
            boxLayout.addWidget(editor)

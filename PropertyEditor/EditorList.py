from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

class __EditorListBase(QWidget):
    dataChanged = pyqtSignal(list)
    shouldSkipLabel = True

    def __init__(self, editorGenerator, targetObject, name):
        super().__init__()

        layout = self._createLayout(name)

        self._targetObject = targetObject
        
        self._createWidgetsForList(layout, editorGenerator, targetObject)

    def _createWidgetsForList(self, boxLayout, editorGenerator, targetList):
        for i in range(len(targetList)):
            name = str(i)

            setter = lambda val, thisI=i: self._setListElem(targetList, thisI, val)

            editor = editorGenerator.createWidget(targetList[i], name, setter)
            editor.dataChanged.connect(self._dataChanged)

            self._addEditorToLayout(editorGenerator, boxLayout, name, editor)

    def _dataChanged(self):
        self.dataChanged.emit(self._targetObject)

    # This is a replacement for this, which isn't valid:
    #  setter = lambda val, thisI=i: targetList[thisI] = val
    def _setListElem(self, targetList, i, val):
        targetList[i] = val

class EditorList(__EditorListBase):
    def __init__(self, editorGenerator, targetObject, name):
        super().__init__(editorGenerator, targetObject, name)

    def _createLayout(self, name):
        selfLayout = QVBoxLayout(self)
        box = QGroupBox(name)
        selfLayout.addWidget(box)
        layout = QVBoxLayout(box)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        return layout

    def _addEditorToLayout(self, editorGenerator, boxLayout, name, editor):
        if hasattr(editor, "shouldSkipLabel") and editor.shouldSkipLabel:
            boxLayout.addWidget(editor)
        else:
            boxLayout.addWidget(editorGenerator.wrapWidgetWithLabel(name, editor))

class EditorListHorizontal(__EditorListBase):
    def __init__(self, editorGenerator, targetObject, name):
        super().__init__(editorGenerator, targetObject, name)

    def _createLayout(self, name):
        selfLayout = QVBoxLayout(self)
        box = QGroupBox(name)
        selfLayout.addWidget(box)
        layout = QHBoxLayout(box)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        return layout

    def _addEditorToLayout(self, editorGenerator, boxLayout, name, editor):
        if hasattr(editor, "shouldSkipLabel") and editor.shouldSkipLabel:
            boxLayout.addWidget(editor)
        else:
            boxLayout.addWidget(QLabel(name))
            boxLayout.addWidget(editor)

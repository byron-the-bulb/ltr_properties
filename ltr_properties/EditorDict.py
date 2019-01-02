from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

from .EditorHeader import EditorHeader

class EditorDict(QWidget):
    dataChanged = pyqtSignal(dict)
    shouldSkipLabel = True

    def __init__(self, editorGenerator, targetObject, name):
        super().__init__()

        selfLayout = QVBoxLayout(self)
        frame = QFrame()
        header = EditorHeader(name, frame)
        selfLayout.addWidget(header)
        selfLayout.addWidget(frame)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._targetObject = targetObject
        
        self._createWidgetsForDict(layout, editorGenerator, targetObject)

    def _createWidgetsForDict(self, boxLayout, editorGenerator, targetDict):
        for name, value in targetDict.items():
            setter = lambda val, thisName=name: self._setDictElem(targetDict, thisName, val)

            editor = editorGenerator.createWidget(value, name, setter)

            if hasattr(editor, "dataChanged"):
                editor.dataChanged.connect(lambda newVal: self._dataChanged())

            if hasattr(editor, "shouldSkipLabel") and editor.shouldSkipLabel:
                boxLayout.addWidget(editor)
            else:
                boxLayout.addWidget(editorGenerator.wrapWidgetWithLabel(name, editor))

    def _dataChanged(self):
        self.dataChanged.emit(self._targetObject)

    # This is a replacement for this, which isn't valid:
    #  setter = lambda val, thisI=i: targetDict[thisName] = val
    def _setDictElem(self, targetDict, name, val):
        targetDict[name] = val

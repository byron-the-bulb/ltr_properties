from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

class EditorDict(QWidget):
    dataChanged = pyqtSignal()
    shouldSkipLabel = True

    def __init__(self, editorGenerator, targetObject, name, labelWidth):
        super().__init__()

        layout = None
        selfLayout = QVBoxLayout(self)
        box = QGroupBox(name)
        selfLayout.addWidget(box)
        layout = QVBoxLayout(box)
        
        self._createWidgetsForDict(layout, editorGenerator, targetObject, labelWidth)

    def _createWidgetsForDict(self, boxLayout, editorGenerator, targetDict, labelWidth):
        for name, value in targetDict.items():
            editor = editorGenerator.createWidget(value, None, name)
            editor.dataChanged.connect(lambda newVal: self._dataChanged(targetDict, name, newVal))

            if hasattr(editor, "shouldSkipLabel") and editor.shouldSkipLabel:
                boxLayout.addWidget(editor)
            else:
                holder = QWidget()
                layout = QHBoxLayout(holder)

                label = QLabel(name)
                label.setFixedWidth(labelWidth)
                layout.addWidget(label)

                layout.addWidget(editor)

                layout.addStretch()

                boxLayout.addWidget(holder)

    def _dataChanged(self, targetDict, name, newVal):
        targetDict[name] = newVal
        self.dataChanged.emit()

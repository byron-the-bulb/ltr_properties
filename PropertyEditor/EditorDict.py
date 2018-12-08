from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

class EditorDict(QWidget):
    dataChanged = pyqtSignal()
    shouldSkipLabel = True

    def __init__(self, editorGenerator, targetObject, name, labelWidth):
        super().__init__()

        selfLayout = QVBoxLayout(self)
        box = QGroupBox(name)
        selfLayout.addWidget(box)
        layout = QVBoxLayout(box)
        
        self._createWidgetsForDict(layout, editorGenerator, targetObject, labelWidth)

    def _createWidgetsForDict(self, boxLayout, editorGenerator, targetDict, labelWidth):
        for name, value in targetDict.items():
            setter = lambda val, thisName=name: self._setDictElem(targetDict, thisName, val)

            editor = editorGenerator.createWidget(value, name, setter)
            editor.dataChanged.connect(lambda newVal: self._dataChanged())

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

    def _dataChanged(self):
        self.dataChanged.emit()

    # This is a replacement for this, which isn't valid:
    #  setter = lambda val, thisI=i: targetDict[thisName] = val
    def _setDictElem(self, targetDict, name, val):
        targetDict[name] = val

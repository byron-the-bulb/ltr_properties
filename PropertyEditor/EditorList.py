from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

class EditorList(QWidget):
    dataChanged = pyqtSignal(list)
    shouldSkipLabel = True

    def __init__(self, editorGenerator, targetObject, name, labelWidth):
        super().__init__()

        selfLayout = QVBoxLayout(self)
        box = QGroupBox(name)
        selfLayout.addWidget(box)
        layout = QVBoxLayout(box)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._targetObject = targetObject
        
        self._createWidgetsForList(layout, editorGenerator, targetObject, labelWidth)

    def _createWidgetsForList(self, boxLayout, editorGenerator, targetList, labelWidth):
        for i in range(len(targetList)):
            name = str(i)

            setter = lambda val, thisI=i: self._setListElem(targetList, thisI, val)

            editor = editorGenerator.createWidget(targetList[i], name, setter)
            editor.dataChanged.connect(self._dataChanged)

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
        self.dataChanged.emit(self._targetObject)

    # This is a replacement for this, which isn't valid:
    #  setter = lambda val, thisI=i: targetList[thisI] = val
    def _setListElem(self, targetList, i, val):
        targetList[i] = val

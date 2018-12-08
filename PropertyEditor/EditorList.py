from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

class EditorList(QWidget):
    dataChanged = pyqtSignal()
    shouldSkipLabel = True

    def __init__(self, editorGenerator, targetObject, name, labelWidth):
        super().__init__()

        layout = None
        selfLayout = QVBoxLayout(self)
        box = QGroupBox(name)
        selfLayout.addWidget(box)
        layout = QVBoxLayout(box)
        
        self._createWidgetsForList(layout, editorGenerator, targetObject, labelWidth)

    def _createWidgetsForList(self, boxLayout, editorGenerator, targetList, labelWidth):
        for i in range(len(targetList)):
            name = str(i)

            editor = editorGenerator.createWidget(targetList[i], None, name)
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
        self.dataChanged.emit()

from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

class EditorSlottedClass(QWidget):
    dataChanged = pyqtSignal(object)
    shouldSkipLabel = True

    def __init__(self, editorGenerator, targetObject, name, labelWidth):
        super().__init__()

        layout = None
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

        self._targetObject = targetObject
        
        self._createWidgetsForObject(layout, editorGenerator, targetObject, labelWidth)

    def _createWidgetsForObject(self, boxLayout, editorGenerator, targetObject, labelWidth):
        for name in targetObject.__slots__:
            # Let users add __dict__ to enable runtime-only data.
            if name == "__dict__":
                continue
                
            setter = lambda val, thisName=name: setattr(targetObject, thisName, val)
            
            editor = editorGenerator.createWidget(getattr(targetObject, name), name, setter)
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

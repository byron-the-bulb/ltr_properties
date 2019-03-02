from PyQt5.QtWidgets import QPushButton, QColorDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.Qt import QColor

# This is a default color editor class that can be used with any color class that supports
# setRgb and getRgb like QColor.
# Should be fairly easy to make it work with other classes as you see fit.
class EditorColor(QPushButton):
    dataChanged = pyqtSignal(object)

    def __init__(self, editorGenerator, targetObject, name, typeHint):
        super().__init__()
        self._editorGenerator = editorGenerator

        self._value = targetObject
        self._updateButtonColor()

        self.clicked.connect(self._pickColor)

    def _pickColor(self):
        dialog = QColorDialog(self)
        dialog.setOption(QColorDialog.DontUseNativeDialog)
        dialog.setStyleSheet("")
        r, g, b = self._value.getRgb()
        dialog.setCurrentColor(QColor(r, g, b))
        if dialog.exec() == QColorDialog.Accepted:
            with self._editorGenerator.threadLock():
                newR, newG, newB, dummy = dialog.currentColor().getRgb()
                if [newR, newG, newB] != [r, g, b]:
                    self._value.setRgb(newR, newG, newB)
                    self.dataChanged.emit(self._value)
                    self._updateButtonColor()

    def _updateButtonColor(self):
        r, g, b = self._value.getRgb()
        self.setStyleSheet("EditorColor {background-color:rgb(" + str(r) + "," + str(g) + "," + str(b) + ")}")

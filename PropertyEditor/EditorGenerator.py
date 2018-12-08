
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox

from .EditorDict import EditorDict
from .EditorFloat import EditorFloat
from .EditorInt import EditorInt
from .EditorList import EditorList
from .EditorSlottedClass import EditorSlottedClass
from .EditorString import EditorString

class EditorGenerator(object):
    def __init__(self, labelWidth, spinBoxWidth):
        self._labelWidth = labelWidth
        self._spinBoxWidth = spinBoxWidth
        pass

    def createWidget(self, value, name = None, changeCallback = None):
        valType = type(value)

        # This set if elifs will either return a widget, or set this to a widget
        # that should then be connected to a setattr lambda to store the value.
        valueEditor = None
        if hasattr(value, "__slots__"):
            if name:
                name = name + " (" + valType.__name__ + ")"
            return EditorSlottedClass(self, value, name, self._labelWidth)
        elif valType == int:
            valueEditor = EditorInt(value, self._spinBoxWidth)
        elif valType == float:
            valueEditor = EditorFloat(value, self._spinBoxWidth)
        elif valType == str:
            valueEditor = EditorString(value)
        elif valType == list:
            return EditorList(self, value, name, self._labelWidth)
        elif valType == dict:
            return EditorDict(self, value, name, self._labelWidth)
        else:
            return QLabel(str(valType) + " is not implemented. If it is a custom class, you need to use __slots__.")

        if changeCallback:
            valueEditor.dataChanged.connect(lambda val: changeCallback(val))
        return valueEditor

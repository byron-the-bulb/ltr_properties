
from PyQt5.QtWidgets import QWidget, QLabel

from .EditorDict import EditorDict
from .EditorFloat import EditorFloat
from .EditorInt import EditorInt
from .EditorList import EditorList
from .EditorSlottedClass import EditorSlottedClass
from .EditorString import EditorString

class EditorGenerator(object):
    def __init__(self, customEditors, labelWidth, spinBoxWidth):
        self._customEditors = customEditors
        self._labelWidth = labelWidth
        self._spinBoxWidth = spinBoxWidth
        pass

    def createWidget(self, value, name = None, changeCallback = None):
        valType = type(value)

        # This set if elifs will either return a widget, or set this to a widget
        # that should then be connected to a setattr lambda to store the value.
        valueEditor = None
        if valType in self._customEditors:
            return self._customEditors[valType](value)
        elif valType == int:
            valueEditor = EditorInt(value, self._spinBoxWidth)
        elif valType == float:
            valueEditor = EditorFloat(value, self._spinBoxWidth)
        elif valType == str:
            valueEditor = EditorString(value)
        elif hasattr(value, "__slots__"):
            valueEditor = EditorSlottedClass(self, value, name, self._labelWidth)
        elif valType == list:
            valueEditor = EditorList(self, value, name, self._labelWidth)
        elif valType == dict:
            valueEditor = EditorDict(self, value, name, self._labelWidth)
        else:
            return QLabel(str(valType) + " is not implemented. If it is a custom class, you need to use __slots__.")

        if changeCallback:
            valueEditor.dataChanged.connect(lambda val: changeCallback(val))
        return valueEditor

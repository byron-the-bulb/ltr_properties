from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import QSize

from .EditorBool import EditorBool
from .EditorDict import EditorDict
from .EditorFloat import EditorFloat
from .EditorInt import EditorInt
from .EditorList import EditorList
from .EditorSlottedClass import EditorSlottedClass
from .EditorString import EditorString

from .HoverableButton import HoverableButton

class EditorGenerator(object):
    def __init__(self, customEditors, labelWidth, spinBoxWidth):
        self._customEditors = customEditors
        self._labelWidth = labelWidth
        self._spinBoxWidth = spinBoxWidth

        self._preLabelWidth = 24
        self._layoutSpacing = 4
        pass

    def createWidget(self, value, name = None, changeCallback = None):
        valType = type(value)

        # This set of elifs will either return a widget, or set this to a widget
        # that should then be connected to a setattr lambda to store the value.
        valueEditor = None
        if valType in self._customEditors:
            return self._customEditors[valType](self, value, name)
        elif valType == bool:
            valueEditor = EditorBool(self, value, name)
        elif valType == int:
            valueEditor = EditorInt(self, value, name)
        elif valType == float:
            valueEditor = EditorFloat(self, value, name)
        elif valType == str:
            valueEditor = EditorString(self, value, name)
        elif hasattr(value, "__slots__"):
            valueEditor = EditorSlottedClass(self, value, name)
        elif valType == list:
            valueEditor = EditorList(self, value, name)
        elif valType == dict:
            valueEditor = EditorDict(self, value, name)
        else:
            return QLabel(str(valType) + " is not implemented.\nIf it is a custom class, you need to use __slots__.")

        if changeCallback:
            valueEditor.dataChanged.connect(lambda val: changeCallback(val))
        return valueEditor

    def createButton(self, icon):
        size = self._preLabelWidth - self._layoutSpacing

        button = HoverableButton(icon, "")
        button.setFixedSize(size, size)
        button.setIconSize(QSize(size, size))

        return button

    def labelWidth(self):
        return self._labelWidth

    def layoutSpacing(self):
        return self._layoutSpacing

    def preLabelWidth(self):
        return self._preLabelWidth

    def spinBoxWidth(self):
        return self._spinBoxWidth

    def wrapWidgetWithLabel(self, name, editor, preLabelWidget=None):
        holder = QWidget()
        layout = QHBoxLayout(holder)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(self._layoutSpacing)

        if preLabelWidget:
            layout.addWidget(preLabelWidget)
        else:
            layout.addSpacing(self._preLabelWidth)

        label = QLabel(name)
        label.setFixedWidth(self._labelWidth)
        layout.addWidget(label)

        layout.addWidget(editor)

        layout.addStretch()

        return holder

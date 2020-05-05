from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import QSize, QObject, pyqtSignal

from enum import Enum

from .EditorBool import EditorBool
from .EditorDict import EditorDict
from .EditorEnum import EditorEnum
from .EditorFloat import EditorFloat
from .EditorInt import EditorInt
from .EditorLink import EditorLink
from .EditorList import EditorList
from .EditorOptional import EditorOptional
from .EditorSlottedClass import EditorSlottedClass
from .EditorString import EditorString
from .EditorVirtualObject import EditorVirtualObject

from .Link import Link
from .VirtualObject import VirtualObjectBase

from .HoverableButton import HoverableButton

from .TypeUtils import checkType, typeHintIsOptional

class EditorGenerator(QObject):
    gotoObject = pyqtSignal(str)

    def __init__(self, customEditors, labelWidth, spinBoxWidth, threadLock, serializer):
        super().__init__()

        self._customEditors = customEditors
        self._labelWidth = labelWidth
        self._spinBoxWidth = spinBoxWidth
        self._threadLock = threadLock
        self._serializer = serializer

        self._preLabelWidth = 24
        self._layoutSpacing = 4
        pass

    def createWidget(self, value, name = None, changeCallback = None, typeHint = None):
        if typeHint:
            checkType(value, typeHint, name)

        valType = type(value)
        # HACK: let us read ints from json as floats in a fairly inelegant way
        if valType == int and typeHint == float:
            valType = float

        # This set of elifs will either return a widget, or set this to a widget
        # that should then be connected to a setattr lambda to store the value.
        valueEditor = None
        if typeHintIsOptional(typeHint):
            valueEditor = EditorOptional(self, value, name, changeCallback, typeHint)
        elif valType in self._customEditors:
            return self._customEditors[valType](self, value, name, typeHint)
        elif valType == bool:
            valueEditor = EditorBool(self, value, name, typeHint)
        elif valType == int:
            valueEditor = EditorInt(self, value, name, typeHint)
        elif valType == float:
            valueEditor = EditorFloat(self, value, name, typeHint)
        elif valType == str:
            valueEditor = EditorString(self, value, name, typeHint)
        elif valType == Link:
            valueEditor = EditorLink(self, value, name, typeHint)
        elif isinstance(value, VirtualObjectBase):
            valueEditor = EditorVirtualObject(self, value, name, typeHint)
        elif hasattr(value, "__slots__"):
            valueEditor = EditorSlottedClass(self, value, name, typeHint)
        elif valType == list:
            valueEditor = EditorList(self, value, name, typeHint)
        elif valType == dict:
            valueEditor = EditorDict(self, value, name, typeHint)
        elif isinstance(value, Enum):
            valueEditor = EditorEnum(self, value, name, typeHint)
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

    def serializer(self):
        return self._serializer

    def spinBoxWidth(self):
        return self._spinBoxWidth

    def threadLock(self):
        return self._threadLock

    def wrapWidget(self, name, editor, preLabelWidget=None):
        holder = QWidget()
        layout = QHBoxLayout(holder)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(self._layoutSpacing)

        if preLabelWidget:
            layout.addWidget(preLabelWidget)
        else:
            layout.addSpacing(self._preLabelWidth)

        if name:
            label = QLabel(name)
            label.setFixedWidth(self._labelWidth)
            layout.addWidget(label)

        layout.addWidget(editor)

        layout.addStretch()

        return holder

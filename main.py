#!/usr/bin/python3

from PropertyEditor.PropertyEditorWidget import PropertyEditorWidget
from PropertyEditor.EditorColor import EditorColor
from PropertyEditor.EditorSlottedClass import EditorSlottedClassHorizontal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea
import sys
import jsonpickle

class Color():
    __slots__ = "r", "g", "b"
    def __init__(self, r, g, b):
        self.setRgb(r, g, b)
    
    def getRgb(self):
        return self.r, self.g, self.b

    def setRgb(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

class Vector():
    __slots__ = "x", "y", "z"
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Baz():
    __slots__ = "x"
    def __init__(self):
        self.x = 10000

class Bar(object):
    __slots__ = "a", "b", "c", "d"
    def __init__(self):
        self.a = {"one": "a", "two": "b"}
        self.b = "two"
        self.c = Color(0, 150, 255)
        self.d = Baz()

class Foo(object):
    __slots__ = "x", "y", "z", "w", "s", "b", "v"
    def __init__(self):
        self.x = 0
        self.y = -25
        self.z = [-100, 20, 3]
        self.w = 0.1
        self.s = "test"
        self.b = Bar()
        self.v = Vector(1, 4, 9)

def onDataChanged(obj):
    print(jsonpickle.dumps(obj))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWidget = QScrollArea()
    mainLayout = QVBoxLayout(mainWidget)
    mainLayout.setContentsMargins(0, 0, 0, 0)

    foo = Foo()

    pe = PropertyEditorWidget()
    pe.registerCustomEditor(Color, EditorColor)
    pe.registerCustomEditor(Vector, EditorSlottedClassHorizontal)
    pe.setTargetObject(foo)

    pe.dataChanged.connect(lambda: onDataChanged(foo))

    mainWidget.setWidget(pe)

    mainWidget.setGeometry(300, 200, 600, 900)
    mainWidget.setWindowTitle('LtRandolph Property Editor')
    mainWidget.show()
    app.exec_()

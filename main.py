#!/usr/bin/python3

from PropertyEditor.PropertyEditorWidget import PropertyEditorWidget
from PropertyEditor.EditorColor import EditorColor
from PropertyEditor.EditorSlottedClass import EditorSlottedClassHorizontal
from PropertyEditor.Serializer import Serializer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea
import sys
import jsonpickle

filename = "mainOutput.json"

def printLoadedClass(obj):
    classDesc = type(obj).__name__ + ":"
    for slot in obj.__slots__:
        classDesc += " " + slot + "=" + str(getattr(obj, slot))
    print("Loaded " + classDesc)

class Color():
    __slots__ = "r", "g", "b"
    def __init__(self, r=0, g=0, b=0):
        self.setRgb(r, g, b)

    def postLoad(self):
        printLoadedClass(self)
    
    def getRgb(self):
        return self.r, self.g, self.b

    def setRgb(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

class Vector():
    __slots__ = "x", "y", "z"
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def postLoad(self):
        printLoadedClass(self)

class Baz():
    __slots__ = "x"
    def __init__(self):
        self.x = 10000

    def postLoad(self):
        printLoadedClass(self)

class Bar(object):
    __slots__ = "a", "b", "c", "d"
    def __init__(self):
        self.a = {"one": "a", "two": "b"}
        self.b = "two"
        self.c = Color(0, 150, 255)
        self.d = Baz()

    def postLoad(self):
        printLoadedClass(self)

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

    def postLoad(self):
        printLoadedClass(self)

def onDataChanged(obj, s):
    s.save(filename, obj)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    s = Serializer(sys.modules[__name__])

    mainWidget = QScrollArea()
    mainLayout = QVBoxLayout(mainWidget)
    mainLayout.setContentsMargins(0, 0, 0, 0)

    foo = None
    try:
        foo = s.load(filename)
    except:
        foo = Foo()

    pe = PropertyEditorWidget()
    pe.registerCustomEditor(Color, EditorColor)
    pe.registerCustomEditor(Vector, EditorSlottedClassHorizontal)
    pe.setTargetObject(foo)

    pe.dataChanged.connect(lambda: onDataChanged(foo, s))

    mainWidget.setWidget(pe)

    mainWidget.setGeometry(300, 200, 600, 900)
    mainWidget.setWindowTitle('LtRandolph Property Editor')
    mainWidget.show()
    app.exec_()

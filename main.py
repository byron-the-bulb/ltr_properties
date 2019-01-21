#!/usr/bin/python3

import ltr_properties
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QScrollArea
import json
import sys

from typing import List, Dict

filename = "data/mainOutput.json"

def printLoadedClass(obj):
    classDesc = type(obj).__name__ + ":"
    for slot in obj.__slots__:
        if hasattr(obj, slot):
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

class FancyBaz(Baz):
    __slots__ = "fanciness"
    fanciness: ltr_properties.Link[Color]

class Bar(object):
    __slots__ = "a", "b", "c", "d", "e", "_hidden"

    # Type hints are optional, but are checked when deserializing. For lists and
    # dicts, they allow empty lists/dicts to be filled with new elements, rather
    # than requiring an existing element to duplicate.
    a: Dict[str, str]
    b: str
    c: List[Color]
    d: List[Vector]
    e: Baz
    def __init__(self):
        self.a = {"one": "a", "two": "b"}
        self.b = "two"
        self.c = [Color(0, 150, 255), Color(), Color(255, 255, 255)]
        self.d = [Vector(), Vector(1, 4, 9), Vector(255, 0, -255)]
        self.e = Baz()
        self._hidden = "Shouldn't show up"

    def postLoad(self):
        printLoadedClass(self)

class Foo(object):
    __slots__ = "x", "y", "z", "w", "s", "b", "v"
    def __init__(self):
        self.x = 0
        self.y = -25.1
        self.z = [-100, 20, 3]
        self.w = True
        self.s = "test"
        self.b = Bar()
        self.v = Vector(1, 4, 9)

    def postLoad(self):
        printLoadedClass(self)

def onDataChanged(obj):
    ltr_properties.Serializer.save(filename, obj, indent=3)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWidget = QWidget()
    mainLayout = QHBoxLayout(mainWidget)

    currentModule = sys.modules[__name__]

    objectTree = ltr_properties.ObjectTree("data")
    sizePolicy = objectTree.sizePolicy()
    sizePolicy.setHorizontalStretch(1)
    objectTree.setSizePolicy(sizePolicy)
    mainLayout.addWidget(objectTree)

    editorWidget = QScrollArea()
    sizePolicy = editorWidget.sizePolicy()
    sizePolicy.setHorizontalStretch(2)
    editorWidget.setSizePolicy(sizePolicy)
    mainLayout.addWidget(editorWidget)

    foo = None
    try:
        foo = ltr_properties.Serializer.load(filename, currentModule)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        foo = Foo()

    pe = ltr_properties.PropertyEditorWidget()
    pe.registerCustomEditor(Color, ltr_properties.EditorColor)
    pe.registerCustomEditor(Vector, ltr_properties.EditorSlottedClassHorizontal)
    pe.setTargetObject(foo)

    pe.dataChanged.connect(lambda: onDataChanged(foo))

    editorWidget.setWidget(pe)

    mainWidget.setGeometry(300, 200, 900, 900)
    mainWidget.setWindowTitle('LtRandolph Property Editor')
    mainWidget.show()
    app.exec_()

#!/usr/bin/python3

from PropertyEditor.PropertyEditorWidget import PropertyEditorWidget
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
import sys
import jsonpickle

class Baz(object):
    __slots__ = "x"
    def __init__(self):
        self.x = 10000

class Bar(object):
    __slots__ = "a", "b", "c", "d"
    def __init__(self):
        self.a = {"one": "a", "two": "b"}
        self.b = "two"
        self.c = "three four five"
        self.d = Baz()

class Foo(object):
    __slots__ = "x", "y", "z", "w", "s", "b"
    def __init__(self):
        self.x = 0
        self.y = -25
        self.z = [-100, 20, 3]
        self.w = 0.1
        self.s = "test"
        self.b = Bar()

def onDataChanged(obj):
    print(jsonpickle.dumps(obj))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWidget = QWidget()
    mainLayout = QVBoxLayout(mainWidget)

    foo = Foo()

    pe = PropertyEditorWidget()
    pe.setTargetObject(foo)

    pe.dataChanged.connect(lambda: onDataChanged(foo))

    mainLayout.addWidget(pe)

    mainWidget.setGeometry(300, 300, 600, 600)
    mainWidget.setWindowTitle('LtRandolph Property Editor')
    mainWidget.show()
    app.exec_()

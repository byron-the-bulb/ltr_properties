import pytest
import pytestqt
import sys
from PyQt5 import QtCore

import ltr_properties

class Bar():
    __slots__ = "i"
    def __init__(self):
        self.i = 0

class Foo():
    __slots__ = "i", "f", "s", "l"
    i: int
    f: float
    s: str
    l: ltr_properties.Link[Bar]
    def __init__(self):
        self.i = 0
        self.f = 0.0
        self.s = ""

def createLtrEditor(qtbot, tmp_path):
    ltrEditor = ltr_properties.LtrEditor(str(tmp_path), sys.modules[__name__])
    qtbot.addWidget(ltrEditor)
    return ltrEditor

def createFooEditor(qtbot, tmp_path):
    ltrEditor = createLtrEditor(qtbot, tmp_path)
    testObj = Foo()
    testPath = "testObj.json"
    ltrEditor.addTargetObject(testObj, "TestObj", testPath)
    objEditor = ltrEditor.editor(testPath)
    return testObj, objEditor

def selectAll(qtbot, editor):
    qtbot.mouseClick(editor, QtCore.Qt.LeftButton)
    qtbot.keyClick(editor, QtCore.Qt.Key_A, QtCore.Qt.ControlModifier)

def testLtrEditorCreate(qtbot, tmp_path):
    assert(createLtrEditor(qtbot, tmp_path))

def testEditInt(qtbot, tmp_path):
    testObj, objEditor = createFooEditor(qtbot, tmp_path)
    iEditor = objEditor.childWidget("i")
    selectAll(qtbot, iEditor)
    qtbot.keyClick(iEditor, QtCore.Qt.Key_2)
    assert(testObj.i == 2)

def testEditFloat(qtbot, tmp_path):
    testObj, objEditor = createFooEditor(qtbot, tmp_path)
    fEditor = objEditor.childWidget("f")
    selectAll(qtbot, fEditor)
    qtbot.keyClick(fEditor, QtCore.Qt.Key_1)
    assert(testObj.f == 1.0)

def testEditString(qtbot, tmp_path):
    testObj, objEditor = createFooEditor(qtbot, tmp_path)
    sEditor = objEditor.childWidget("s")
    qtbot.keyClicks(sEditor, "hello sailor")
    qtbot.keyClick(sEditor, QtCore.Qt.Key_Enter)
    assert(testObj.s == "hello sailor")

def testEditLink(qtbot, monkeypatch, tmp_path):
    testObj, objEditor = createFooEditor(qtbot, tmp_path)
    lEditor = objEditor.childWidget("l")

    monkeypatch.setattr(
        ltr_properties.EditorLink.EditorLink, "_chooseFile", classmethod(lambda *args: "test.json")
    )

    with open(tmp_path / "test.json", "w") as tempFile:
        tempFile.write('{"Bar": {"i": 15}}')

    qtbot.mouseClick(lEditor._openButton, QtCore.Qt.LeftButton)
    assert(testObj.l.filename == "test.json")
    assert(testObj.l.i == 15)

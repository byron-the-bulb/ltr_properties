from .Link import Link
from .UIUtils import clearLayout
from .TypeUtils import getDictKVTypeHints
import typing

from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QGridLayout, QFileDialog, QMenu, QMessageBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import pyqtSignal

import os

class EditorLinkMap(QWidget):
    dataChanged = pyqtSignal(object)

    def __init__(self, editorGenerator, targetObject, name, typeHint):
        super().__init__()
        self._editorGenerator = editorGenerator

        self._targetObject = targetObject
        self._valueTypeHint = getDictKVTypeHints(typing.get_type_hints(type(targetObject))[self.getMapAttr()])[1]
        self._mainLayout = QGridLayout(self)
        self.createWidgetsForObject()

    def createWidgetsForObject(self):
        self._currentCol = 0
        clearLayout(self._mainLayout)
        self.addColumn(self.makeBaseHeader(), self.makeBaseEditor())
        for key, value in self._getMap().items():
            self.addColumn(self.makeMapHeader(key), self.makeMapEditor(key))
        if self.getBonusAttr():
            self.addColumn(QLabel(self.getBonusAttr()), self.makeBonusEditor())
        self._mainLayout.addItem(QSpacerItem(1, 1, hPolicy=QSizePolicy.Expanding), 0, self._currentCol)

    def getBonusAttr(self):
        return None

    def getBaseAttr(self):
        return None

    def getMapAttr(self):
        return None

    def getDefaultPath(self):
        return ""

    def constructValue(self):
        return self._valueTypeHint(1)

    def makeMapHeader(self, key):
        header = QPushButton(key)
        header.setMaximumWidth(200)
        header.setToolTip(key)
        menu = QMenu(header)
        header.setMenu(menu)
        menu.addAction("Replace", lambda thisKey=key: self.replaceMapElem(thisKey))
        menu.addAction("Delete", lambda thisKey=key: self.deleteMapElem(thisKey))
        return header

    def makeMapEditor(self, key):
        setter = lambda val, thisKey=key: self._setMapElem(thisKey, val)
        return self.makeEditor(setter, self._getMap()[key], self._valueTypeHint)

    def makeBaseHeader(self):
        baseAttr = self.getBaseAttr()
        header = QPushButton("Base" if baseAttr else "Add")
        header.setMaximumWidth(100)
        menu = QMenu(header)
        header.setMenu(menu)
        menu.addAction("Add", self.addMapElem)
        return header

    def makeBaseEditor(self):
        baseAttr = self.getBaseAttr()
        if baseAttr:
            setter = lambda val: setattr(self._targetObject, baseAttr, val)
            typeHint = typing.get_type_hints(type(self._targetObject))[baseAttr]
            return self.makeEditor(setter, getattr(self._targetObject, baseAttr), typeHint)
        else:
            return None

    def makeBonusEditor(self):
        bonusAttr = self.getBonusAttr()
        setter = lambda val: setattr(self._targetObject, bonusAttr, val)
        typeHint = typing.get_type_hints(type(self._targetObject))[bonusAttr]
        return self.makeEditor(setter, getattr(self._targetObject, bonusAttr), typeHint)

    def makeEditor(self, setter, value, typeHint):
        editor = self._editorGenerator.createWidget(value, "", setter, typeHint=typeHint)

        if hasattr(editor, "dataChanged"):
            editor.dataChanged.connect(self._dataChanged)

        return editor

    def addColumn(self, top, bottom=None):
        self._mainLayout.addWidget(top, 0, self._currentCol)
        if bottom:
            self._mainLayout.addWidget(bottom, 1, self._currentCol)
        self._currentCol += 1

    def addMapElem(self):
        newTarget = self.chooseNewKey()
        if newTarget:
            self._getMap()[newTarget] = self.constructValue()
            self._dataChanged()
            self.createWidgetsForObject()

    def deleteMapElem(self, key):
        if QMessageBox.question(self, "Delete?", "Delete " + key + "?") == QMessageBox.Yes:
            del(self._getMap()[key])
            self._dataChanged()
            self.createWidgetsForObject()

    def replaceMapElem(self, oldTarget):
        newTarget = self.chooseNewKey()
        if newTarget and oldTarget != newTarget:
            self._getMap()[newTarget] = self._getMap()[oldTarget]
            del(self._getMap()[oldTarget])
            self._dataChanged()
            self.createWidgetsForObject()

    def chooseNewKey(self):
        rootPath = os.path.join(self._editorGenerator.serializer().root(), self.getDefaultPath())
        filename = QFileDialog.getOpenFileName(self, "New Element", rootPath, "*.json")
        if filename[0]:
            newPath = os.path.relpath(filename[0], rootPath)
            if ".." in newPath:
                QMessageBox.warning(self, "Invalid Path", os.path.abspath(newPath) + "\n\nis outside the root path\n\n" + os.path.abspath(rootPath))
                return None

            newTarget = os.path.basename(newPath).replace(".json", "")
            if newTarget in self._getMap():
                QMessageBox.warning(self, "Already have " + newTarget + "!")
                return None
            return newTarget

        return None

    def _dataChanged(self):
        self.dataChanged.emit(self._targetObject)

    # This is a replacement for this, which isn't valid:
    #  setter = lambda val, thisI=i: targetDict[thisName] = val
    def _setMapElem(self, key, val):
        self._getMap()[key] = val

    def _getMap(self):
        mapAttr = self.getMapAttr()
        if mapAttr != None:
            return getattr(self._targetObject, mapAttr)
        else:
            return self._targetObject

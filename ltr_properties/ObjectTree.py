from .AddObjectDialog import AddObjectDialog
from .DuplicateObjectDialog import DuplicateObjectDialog
from .RenameDialog import RenameDialog

from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QMenu, QAction, QInputDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt

import json
import os
import shutil

class ObjectTree(QTreeView):
    fileActivated = pyqtSignal(str, str)
    pathDeleted = pyqtSignal(str)

    def __init__(self, rootPath, classDict, iconProvider):
        super().__init__()

        self._classDict = classDict

        self._model = QFileSystemModel(self)
        self._model.setNameFilters(["*.json"])
        self._model.setNameFilterDisables(False)
        if iconProvider:
            self._model.setIconProvider(iconProvider)
        self.setModel(self._model)
        self.setSortingEnabled(True)
        self.sortByColumn(0, Qt.AscendingOrder)
        self.setRootPath(rootPath)

        for i in range(self._model.columnCount()):
            if i != 0:
                self.setColumnHidden(i, True)

        self.activated.connect(self._onActivated)

    def rootPath(self):
        return self.model().rootPath()

    def setRootPath(self, rootPath):
        self.setRootIndex(self.model().setRootPath(rootPath))
        self.expandAll()

    def contextMenuEvent(self, event):
        clickedIndex = self.indexAt(event.pos())

        rootPath = self.model().rootPath()

        clickedPath = self.model().filePath(clickedIndex) if clickedIndex.isValid() else rootPath
        # Figure out where we should put any new objects or folders.
        containingPath = os.path.dirname(clickedPath) if os.path.isfile(clickedPath) else clickedPath

        clickedPath = os.path.abspath(clickedPath)
        containingPath = os.path.abspath(containingPath)

        menu = QMenu(self)
        menu.addAction("Add Object", lambda: self._addObject(containingPath))
        menu.addAction("Add Folder", lambda: self._addFolder(containingPath))

        if clickedIndex.isValid():
            menu.addSeparator()
            if os.path.isfile(clickedPath):
                menu.addAction("Duplicate Object", lambda: self._duplicateObject(clickedPath))
                menu.addAction("Delete Object", lambda: self._deleteObject(clickedPath))
                menu.addAction("Rename Object", lambda: self._renameObject(clickedPath))
            else:
                menu.addAction("Delete Folder", lambda: self._deleteFolder(clickedPath))
                menu.addAction("Rename Folder", lambda: self._renameFolder(clickedPath))

        action = menu.exec_(self.mapToGlobal(event.pos()))

    def _addFolder(self, containingPath):
        text, ok = QInputDialog.getText(self, "New Folder", containingPath + "/")

        # Do some very mild validity checking, then just try to make the folder.
        if ok:
            if '/' in text or '\\' in text:
                QMessageBox.warning(self, "Path error", "Cannot use slashes in path:\n" + text)
                return

            try:
                os.mkdir(os.path.join(containingPath, text))
            except OSError as e:
                QMessageBox.warning(self, "Failed to make folder", str(e))

    def _addObject(self, containingPath):
        dialog = AddObjectDialog(self._classDict, containingPath, self)
        result = dialog.exec()
        if result == AddObjectDialog.Accepted:
            destPath = os.path.join(containingPath, dialog.name() + ".json")
            if os.path.exists(destPath):
                QMessageBox.warning(self, "Already exists", destPath + " already exists")
                return
            try:
                with open(destPath, 'w') as outFile:
                    outFile.write(json.JSONEncoder().encode({dialog.objClass(): {}}))
                
                name = os.path.basename(destPath).replace(".json", "")
                self.fileActivated.emit(name, destPath)                
            except OSError as e:
                QMessageBox.warning(self, "Failed to make object", str(e))

    def _duplicateObject(self, oldPath):
        shortPath = os.path.relpath(oldPath, self.rootPath())
        shortPath = shortPath.replace(".json", "")
        dialog = DuplicateObjectDialog(shortPath, self)
        result = dialog.exec()
        if result == DuplicateObjectDialog.Accepted:
            destPath = os.path.join(self.rootPath(), dialog.path() + ".json")
            if os.path.exists(destPath):
                QMessageBox.warning(self, "Already exists", destPath + " already exists")
                return
            try:
                shutil.copyfile(oldPath, destPath)

                name = os.path.basename(destPath).replace(".json", "")
                self.fileActivated.emit(name, os.path.relpath(destPath, self.rootPath()))
            except OSError as e:
                QMessageBox.warning(self, "Failed to make object", str(e))

    def _deleteFolder(self, path):
        reply = QMessageBox.question(self, "Delete?", "Delete folder and all its contents?\n" + path,
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            shutil.rmtree(path)
            self.pathDeleted.emit(path)

    def _deleteObject(self, path):
        reply = QMessageBox.question(self, "Delete?", "Delete object?\n" + path,
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            os.unlink(path)
            self.pathDeleted.emit(path)

    def _renameFolder(self, oldPath):
        shortPath = os.path.relpath(oldPath, self.rootPath())
        dialog = RenameDialog(shortPath, self)
        result = dialog.exec()
        if result == RenameDialog.Accepted:
            destPath = os.path.join(self.rootPath(), dialog.path())
            if os.path.exists(destPath):
                QMessageBox.warning(self, "Already exists", destPath + " already exists")
                return
            try:
                shutil.move(oldPath, destPath)
            except OSError as e:
                QMessageBox.warning(self, "Failed to rename folder", str(e))

    def _renameObject(self, oldPath):
        shortPath = os.path.relpath(oldPath, self.rootPath())
        shortPath = shortPath.replace(".json", "")
        dialog = RenameDialog(shortPath, self)
        result = dialog.exec()
        if result == RenameDialog.Accepted:
            destPath = os.path.join(self.rootPath(), dialog.path() + ".json")
            if os.path.exists(destPath):
                QMessageBox.warning(self, "Already exists", destPath + " already exists")
                return
            try:
                shutil.move(oldPath, destPath)
                self.pathDeleted.emit(oldPath)

                name = os.path.basename(destPath).replace(".json", "")
                self.fileActivated.emit(name, destPath)
            except OSError as e:
                QMessageBox.warning(self, "Failed to rename object", str(e))

    def _onActivated(self, index):
        if self._model.isDir(index):
            return
        path = os.path.relpath(self._model.filePath(index), self.rootPath())
        name = self._model.fileName(index)
        name = name.replace(".json", "")
        self.fileActivated.emit(name, path)

from PyQt5.QtWidgets import QTreeView, QFileSystemModel
from PyQt5.QtCore import pyqtSignal

class ObjectTree(QTreeView):
    fileActivated = pyqtSignal(str, str)

    def __init__(self, rootPath):
        super().__init__()
        self._model = QFileSystemModel(self)
        self._model.setNameFilters(["*.json"])
        self._model.setNameFilterDisables(False)
        self.setModel(self._model)
        self.setSortingEnabled(True)
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

    def _onActivated(self, index):
        path = self._model.filePath(index)
        name = self._model.fileName(index)
        name = name.replace(".json", "")
        self.fileActivated.emit(name, path)

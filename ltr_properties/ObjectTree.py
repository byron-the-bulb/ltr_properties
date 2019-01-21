from PyQt5.QtWidgets import QTreeView, QFileSystemModel

class ObjectTree(QTreeView):
    def __init__(self, rootPath):
        super().__init__()
        model = QFileSystemModel(self)
        model.setNameFilters(["*.json"])
        model.setNameFilterDisables(False)
        self.setModel(model)
        self.setSortingEnabled(True)
        self.setRootPath(rootPath)

        for i in range(model.columnCount()):
            if i != 0:
                self.setColumnHidden(i, True)

    def rootPath(self):
        return self.model().rootPath()

    def setRootPath(self, rootPath):
        self.setRootIndex(self.model().setRootPath(rootPath))
        self.expandAll()

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QLineEdit, QDialogButtonBox, QLabel

class AddObjectDialog(QDialog):
    def __init__(self, classDict, path, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Object")

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Class"))

        classList = list(classDict.keys())
        classList.remove("Link")
        classList.sort()

        self._comboBoxClass = QComboBox()
        self._comboBoxClass.addItems(classList)
        layout.addWidget(self._comboBoxClass)

        layout.addWidget(QLabel("Path"))
        layout.addWidget(QLabel(path))
        self._lineEditName = QLineEdit()
        layout.addWidget(self._lineEditName)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def objClass(self):
        return self._comboBoxClass.currentText()

    def name(self):
        return self._lineEditName.text()

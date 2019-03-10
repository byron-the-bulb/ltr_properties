from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QLineEdit, QDialogButtonBox, QLabel

class DuplicateObjectDialog(QDialog):
    def __init__(self, path, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Duplicate Object")

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Source: " + path))

        layout.addWidget(QLabel("New Path"))
        self._lineEditPath = QLineEdit(path)
        layout.addWidget(self._lineEditPath)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def path(self):
        return self._lineEditPath.text()

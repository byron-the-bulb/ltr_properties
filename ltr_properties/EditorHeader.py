from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QFrame, QSizePolicy
from PyQt5.QtCore import QSize

from .HoverableButton import HoverableButton
from .Icons import Icons

class EditorHeader(QWidget):
    def __init__(self, name, hideableWidget, preLabelWidth, extraWidgets=[]):
        super().__init__()

        self.hideableWidget = hideableWidget

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        buttonSize = preLabelWidth - layout.spacing()

        self.expandButton = HoverableButton(Icons.ArrowDown, "")
        self.expandButton.setFixedSize(buttonSize, buttonSize)
        self.expandButton.setIconSize(QSize(buttonSize, buttonSize))
        self.expandButton.setCheckable(True)
        self.expandButton.setChecked(True)
        layout.addWidget(self.expandButton)
        self.expandButton.clicked.connect(self._expandButtonClicked)

        layout.addWidget(QLabel(name))

        for extraWidget in extraWidgets:
            layout.addWidget(extraWidget)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        layout.addWidget(line)

    def _expandButtonClicked(self):
        isChecked = self.expandButton.isChecked()
        self.expandButton.setIcon(Icons.ArrowDown if isChecked else Icons.ArrowRight)
        self.hideableWidget.setVisible(isChecked)

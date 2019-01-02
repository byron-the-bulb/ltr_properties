from PyQt5.QtWidgets import QPushButton

class HoverableButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("""
            QPushButton {border: none;}
            QPushButton:hover {background: solid rgb(91,231,255);}
            """)

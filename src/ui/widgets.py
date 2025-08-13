from PyQt5.QtWidgets import QPushButton, QFrame
from PyQt5.QtGui import QFont


class SimpleButton(QPushButton):
    """Botão simples"""

    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setFont(QFont("Segoe UI", 10))
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #667eea;
                border: none;
                border-radius: 6px;
                color: white;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #5a6fd8; }
            QPushButton:pressed { background-color: #4a5fc6; }
            """
        )


class SimpleCard(QFrame):
    """Card simples"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e1e5e9;
            }
            """
        )


